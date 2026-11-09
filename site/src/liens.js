// Adresse de la page dédiée de chaque formation (générée au build par scripts/prerender.mjs).
// Partagé par l'application et le pré-rendu : un seul calcul, aucune page orpheline.
export const titreCourt = (t) => String(t || '').split(' : ')[0].trim()

export function slugFormation(f) {
  const nom = titreCourt(f.titre)
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/&/g, ' et ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
  return `formations/${f.ref.toLowerCase()}-${nom}.html`
}
