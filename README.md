BASE – Revenu Universel Décentralisé

BASE n’est pas une aide sociale, c’est un droit économique.

BASE est une crypto-monnaie universelle inspirée de Bitcoin mais conçue pour distribuer un revenu minimal à chaque individu dès sa naissance.

1️⃣ Résumé exécutif

Flux universel automatique pour chaque wallet.

Transactions rapides, simples et peu énergivores.

Sécurité via PoW léger et signatures Ed25519.

Interface web locale pour consulter et envoyer BASE.

Sauvegarde rolling des 10 derniers cycles pour sécurité.

2️⃣ Objectifs

Garantir un revenu minimal à tout utilisateur.

Créer un système décentralisé et sécurisé.

Permettre l’utilisation dans des services ou biens réels.

Maintenir la stabilité économique du réseau BASE.

3️⃣ Architecture technique
3.1 Blockchain (Layer 1)

Minage léger CPU toutes les 30 secondes.

Ajout des blocs contenant transactions et flux universel.

Sauvegarde des 10 derniers cycles pour reprise en cas de problème.

3.2 Flux universel
Statut	Flux mensuel	% utilisable	Commentaire
Child	750 B	50%	jusqu’à 18 cycles (~18 ans)
Ado	1000 B	60%	de 18 à 36 cycles
Adult	1500 B	80%	à partir de 36 cycles

Les fonds sont utilisables immédiatement selon le pourcentage indiqué.

Passage automatique Child → Ado → Adult.

Accumulation même en inactivité.

3.3 Transactions (Layer 2)

Frais minimes pour réseau et créateur à vie.

Signatures Ed25519 pour sécurité.

API REST disponible pour envoi et consultation de BASE.

3.4 Wallets

Création automatique à la première connexion (/wallet/ui).

Export et import de wallet possible via API :

/wallet/export

/wallet/import

Interface web locale pour consulter solde et historique :

http://127.0.0.1:5000/wallet/ui

4️⃣ Déploiement
4.1 Installation des dépendances
python -m pip install flask pynacl waitress

4.2 Lancer le node
python Base_Final.py


Node prêt à fonctionner avec flux automatique.

Interface web : http://127.0.0.1:5000/wallet/ui

API disponible :

/chain → récupérer la blockchain

/send_tx → envoyer des BASE

5️⃣ Sauvegarde et reprise

Sauvegarde rolling des 10 derniers cycles dans le dossier backups.

Permet de restaurer la blockchain et les wallets en cas de problème.

6️⃣ Export / Import Wallet

Exporter son wallet pour sauvegarde personnelle :

POST /wallet/export
{
  "wallet": "ID_WALLET"
}


Importer un wallet existant pour retrouver ses fonds :

POST /wallet/import
{
  "wallet": "ID_WALLET",
  "sk": "CLE_PRIVEE_HEX",
  "status": "adult"
}

7️⃣ Roadmap

Phase 1 – Test local

Node sur PC personnel ou VPS.

Validation des flux universels et transactions.

Phase 2 – Test public

Lancement de quelques nodes pour test réseau.

Validation discovery automatique et multi-node.

Phase 3 – Production

Publication GitHub + site officiel.

Intégration avec services/DEX pour échange.

8️⃣ Notes

Chaque utilisateur peut recevoir son flux mensuel automatiquement dès la création de son wallet.

Les fonds sont sécurisés via signatures et sauvegardes.

La valeur économique dépendra de l’adoption et des échanges dans la vie réelle ou via DEX.
