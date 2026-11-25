/**
 * Adaptateur Brevo pour Comp AI (remplace Resend, hébergé aux États-Unis).
 *
 * Brevo (Sendinblue SAS, Paris) : API transactionnelle
 * POST https://api.brevo.com/v3/smtp/email — en-tête `api-key`.
 * Doc : https://developers.brevo.com/reference/sendtransacemail
 *
 * Expose la même forme que le SDK Resend utilisé par Comp
 * (`emails.send` et `batch.send`), pour ne modifier que l'initialisation.
 * Licence : AGPL-3.0, comme Comp AI (modification publiée dans ce dépôt).
 */

type Adresse = { email: string; name?: string };

export interface ResendLikePayload {
  from: string;
  to: string | string[];
  cc?: string | string[];
  bcc?: string | string[];
  replyTo?: string | string[];
  subject: string;
  html?: string;
  text?: string;
  react?: unknown;
  headers?: Record<string, string>;
  scheduledAt?: string;
  attachments?: { filename: string; content: Buffer | string; contentType?: string }[];
}

type Resultat = { data: { id: string } | null; error: { message: string } | null };

/** « Nom <email@domaine> » ou « email@domaine » → { email, name } */
export function parseAdresse(valeur: string): Adresse {
  const m = valeur.match(/^\s*"?([^"<]*?)"?\s*<([^>]+)>\s*$/);
  if (m) return m[1] ? { name: m[1].trim(), email: m[2].trim() } : { email: m[2].trim() };
  return { email: valeur.trim() };
}

function liste(v?: string | string[]): Adresse[] | undefined {
  if (!v) return undefined;
  const items = (Array.isArray(v) ? v : v.split(',')).map((s) => s.trim()).filter(Boolean);
  return items.length ? items.map(parseAdresse) : undefined;
}

function enBase64(content: Buffer | string): string {
  if (typeof content !== 'string') return content.toString('base64');
  // Resend accepte déjà du base64 en chaîne : on le transmet tel quel.
  return content;
}

async function rendreHtml(p: ResendLikePayload): Promise<string | undefined> {
  if (p.html) return p.html;
  if (!p.react) return undefined;
  const { render } = await import('@react-email/render');
  // render() est asynchrone depuis @react-email/render v1
  return await (render as (n: unknown) => Promise<string> | string)(p.react);
}

export class BrevoMailer {
  private readonly url = 'https://api.brevo.com/v3/smtp/email';

  constructor(private readonly apiKey: string) {}

  private async envoyer(p: ResendLikePayload): Promise<Resultat> {
    try {
      const htmlContent = await rendreHtml(p);
      const corps: Record<string, unknown> = {
        sender: parseAdresse(p.from),
        to: liste(p.to),
        cc: liste(p.cc),
        bcc: liste(p.bcc),
        replyTo: liste(p.replyTo)?.[0],
        subject: p.subject,
        htmlContent,
        textContent: p.text,
        headers: p.headers,
        scheduledAt: p.scheduledAt,
        attachment: p.attachments?.map((a) => ({ name: a.filename, content: enBase64(a.content) })),
      };
      for (const k of Object.keys(corps)) if (corps[k] === undefined) delete corps[k];
      if (!corps.htmlContent && !corps.textContent) {
        return { data: null, error: { message: 'Brevo : contenu du message vide (html, text ou react requis)' } };
      }

      const rep = await fetch(this.url, {
        method: 'POST',
        headers: { 'api-key': this.apiKey, 'content-type': 'application/json', accept: 'application/json' },
        body: JSON.stringify(corps),
      });
      const json = (await rep.json().catch(() => ({}))) as { messageId?: string; message?: string };
      if (!rep.ok) {
        return { data: null, error: { message: `Brevo ${rep.status} : ${json.message ?? rep.statusText}` } };
      }
      return { data: { id: json.messageId ?? '' }, error: null };
    } catch (e) {
      return { data: null, error: { message: e instanceof Error ? e.message : String(e) } };
    }
  }

  emails = {
    send: (p: ResendLikePayload) => this.envoyer(p),
  };

  batch = {
    // Brevo n'a pas d'envoi groupé hétérogène : un appel par message, dans l'ordre.
    send: async (payloads: ResendLikePayload[], _opts?: unknown) => {
      const ids: { id: string }[] = [];
      for (const p of payloads) {
        const r = await this.envoyer(p);
        if (r.error) return { data: ids.length ? { data: ids } : null, error: r.error };
        ids.push({ id: r.data?.id ?? '' });
      }
      return { data: { data: ids }, error: null };
    },
  };
}
