## LeagueX on Web 3
#### Fantasy Sports and Gaming on the Open Web using Algorand Blockchain

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
3. Querying for the league leaderboard at any given time






