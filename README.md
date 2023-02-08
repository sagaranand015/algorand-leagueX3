## LeagueX on Web 3
#### Fantasy Sports and Gaming on the Open Web using Algorand Blockchain

A fantasy sport is a form of game, commonly played on the Internet, in which participants assemble imagined, or virtual teams made up of proxies for genuine professional athletes. These gamers qualify based on their players’ statistical performance in actual games. This performance is transformed into points, which are collated and totaled based on a roster chosen by the manager of each fantasy club. These point systems can be simple enough to be computed manually by a “league commissioner” (blockchain in this case) who supervises and controls the overall league, or they can be collated and calculated using computers that follow genuine professional sport results. In fantasy sports, club owners, like in actual sports, draft, trade, and cut (drop) players. Fantasy sports began in traditional sports like cricket and have recently made their way into esports.

LeagueX3 is the fantasy gaming platform hosted on the Algorand Blockchain to let Algorand users participate in the fantasy game of their choice. LeagueX3 is a series of smart contracts deployed on Algorand, that allows management of fanatsy leagues, user squads participating in leagues, managing leaderboards for several leagues and so on. 
LeagueX3 aims to become the single stop solution for all fanatsy games hosted on the Algorand blockchain and provide users with the fun of fantasy gaming in the world of OpenWeb and CrypoCurrencies

### DataStores
1. We use IPFS and Algorand blockchain to host the seed data required for any conducting any fantasy sports event. 
2. The approach involves:
    a. Creating IPFS based data stores for a team under every sport. 
    b. Creating a Smart Contract(aka app) per supported sport and storing the initial seed data (coming from IPFS) on the Algorand blockchain
    c. This data remains public and will be used by both LeagueX3 and players to create their participating squads. 
    d. Note: We use Algorand Box Storage to store every team's IPFS based data

### Squads and Leagues
*Abstract*: Fantasy Gaming involves creating squads based on actual matches and participating in leagues with the best squads. Important features of a Fantasy Gaming Organization involves:
1. Creating and Managing player squads for any given competition(aka match)
2. Creating/Managing Leagues, Managing participation of squads in the leagues, managing/updating the league leaderboards for all participating squads at all times. 

*Approach*: We use IPFS and Algorand Blockchain to store the Squads Data and compute the Leagues leaderboard data on the blockchain itself. This involves:
1. Allowing users to create and manage their squads for any given competition. 
2. Allowing users to participate in a league
3. Querying for the league leaderboard at any given time [TODO]

### Smart Contracts
We use algorand Smart Contracts to manage 
1. the datastores for a fantasy sport (See contracts/cricket_datastore.py)
2. the leagues (as algorand apps) for each competition (See contracts/leagueX3.py)

### Workflow
1. The Deployed Smart contracts work on two levels:
    a. Datastore Smart Contract to store the available players for a sport and to store the squads created by a user
    b. LeagueX3 Smart Contract to store the user's league participation data on Algorand blockchain and to manage/update the leaderboard associated with that league
2. There is a python backend to interface with the deployed smart contracts
3. The frontend (based on Nextjs) interfaces with the python backend to talk to the Algorand blockchain and execute transactions on user's behalf

### TODO Items
This project only demonstrates the use of Algorand Blockchain for creating and managing fantasy sports on Web3. The following are the pending items for an entire implementation of this project:
    a. Allow users to participate in leagues with a pre-defined amount of Algorand Tokens (just like any other currency)
    b. Computing the league's leaderboard as and when the league is in progress

### Initializing the frontend
```
cd frontend
yarn
yarn dev
```
After running these commands from repo root, the frontend should be served at http://localhost:3000/

### Initializing the python backend
```
export SERVER_SECRET_KEY=<my-secret-key>
pip install -r requirements.txt
python3 -m server
```
After running these commands from repo root, the backend server should be served at http://localhost:8080/






