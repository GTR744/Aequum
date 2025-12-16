# BASE – Revenu Universel Décentralisé

## 1️⃣ Résumé exécutif
BASE est une crypto-monnaie universelle inspirée de Bitcoin mais conçue pour un revenu universel.
Chaque être humain peut recevoir un flux automatique de BASE dès sa naissance, garantissant un droit économique plutôt qu’une aide.

Objectifs :
- Redistribution équitable à chaque individu
- Sécurité et décentralisation via PoW léger CPU
- Transactions rapides et simples
- Système transparent pour éviter toute fraude

## 2️⃣ Flux universel
| Catégorie | Flux par mois | % utilisable |
|-----------|---------------|--------------|
| Adulte    | 1500 B        | 80%          |
| Enfant    | 750 B         | 50%          |

- Blocage partiel des fonds pour les enfants
- Déblocage progressif

## 3️⃣ Transactions et frais
- Frais minimes pour maintenir l’infrastructure
- Transactions signées avec Ed25519
- Transferts rapides, validés par PoW léger CPU

## 4️⃣ Sécurité
- Wallets uniques + clés Ed25519
- Flux limité par cycle et âge
- PoW léger pour empêcher spam/attaques

## 5️⃣ Déploiement

### 5.1 Installation des dépendances
```bash
python -m pip install flask pynacl waitress

## 5.2 Lancer votre node !
python BASE_PROD.py

#5.3 API

Voir blockchain :

GET http://127.0.0.1:5000/chain

Envoyer B :

POST http://127.0.0.1:5000/send_tx
Content-Type: application/json

{
  "from": "WALLET_ID_FROM",
  "to": "WALLET_ID_TO",
  "amount": 100
}

## 6️⃣ Roadmap

1. Test local (PC/VPS)

2. Test public multi-node

3. Publication globale (GitHub + site officiel)

4. Applications paiement et intégration services/biens
