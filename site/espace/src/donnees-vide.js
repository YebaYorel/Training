// Remplace donnees.js dans les versions publiées (studio, aperçu) : aucun lien Airtable interne n'y figure.
export const proxyDisponible = async () => false
export const chargerDirect = async () => {
  throw new Error('Indisponible dans cette version.')
}
