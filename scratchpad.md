## Scratchpad

### 0. Teams and Players Datastore [SC DONE]
Define a datastore that will contain a list of all sports, their available teams and available players (and their ratings) within each team. This info can then be used by other smart contracts that interact with squads, leagues or leaderboards. 

### 1. Pick a Squad (for each match)
A Squad is a list of players defined by the user for each match. A player can have multiple squads for a single match, however only a single entry can be done to a league (ie, only 1 squad will be in use at any given time)
#### Questions: 
1. Does this squad info go on blockchain? or on IPFS?
    A: What if there is a leagueX smart contract (for every league?) that registers the squads of all participating users and stores it in the application state?
#### Approach
1. Create a Squad Smart Contract that will be responsible for:
    a. Providing the available players from all available teams (for a sport)
    b. Creating and Managing squads for registered users
2. Use Global application state for maintaining supported sports
3. Use Box storage for storing squads and their users. (Is update to box storage supported in Algorand?)
4. Write functions to manage everything related to a user's squad


### 2. Join a league (for each match)
A league is basically a collection of squads, against a physical match and its parameters. As the match progresses, the league should be responsible for calculating squad scores against a pre-defined set of rules and provide a leaderboard for the registered squads. 
A league can be represented as an app on the algorand blockchain, so all operations within a league are localized to its own app. This app (SC essentially) would be responsible for registering the users and their squads on the algorand blockchain and compute the leaderboard based on the actual match parameters.
The application state can be used to keep track of the leaderboard for the user. (Maybe even relay the final updates to the Squad SC using [1]??)
#### Questions:
1. How is the leaderboard calculated while the match is in progress?
    A: The leagueX org should be responsible for updating the leaderboard for every running league and make sure the application state (containing all squads and their data) is up to date at regular intervals. 
#### Approach:
1. Create a League Smart Contract that will be responsible for:
    a. Creating a league for a given sport
    b. Registering users and their chosen squad to the league
    c. Managing and updating the leaderboard for the league
    d. Returning and exposing leaderboard operations for the league

### 3. Follow the leaderboard
Reading the leaderboard from the league app is easy and can be done using a simple get call. 



### 4. Win and Withdraw
Based on the pre-defined league rules, various squads from the leaderboard are awarded NFTs (ie Algorand ASAs) for that league. 