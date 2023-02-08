import { FetchDataFromIpfsLink } from "./nftStorage"

export async function getUserSquadData(authToken: string | null) {
    console.log("auth toke is: Bearer ", authToken)
    if (authToken) {
        var resp = await fetch('http://localhost:8080/squads/all', {
            method: "GET",
            headers: {
                'Authorization': "Bearer " + authToken
            }
        })
        var dataResp = await resp.json()

        const squadIpfs = dataResp.squads
        console.log("====== api response ois:  ", squadIpfs)
        if (squadIpfs) {
            const data: string = FetchDataFromIpfsLink(squadIpfs)
            const resp = await fetch(data)
            console.log("====== data is:  ", data, resp)
            var squadDataResp = await resp.json()
            console.log("====== ipfs gateway response ois:  ", squadDataResp)
            return squadDataResp
        }
    }
}

export async function ParticipateWithUserAddress(authToken: string | null, league_data: string, squad_data: string) {
    console.log("auth toke is: Bearer ", authToken)
    if (authToken) {
        var resp = await fetch('http://localhost:8080/leagues/participate', {
            method: "POST",
            body: JSON.stringify({
                "league_data": league_data,
                "squad_data": squad_data
            }),
            headers: {
                'Authorization': "Bearer " + authToken,
                'Content-Type': 'application/json',
            }
        })
        var dataResp = await resp.json()
        console.log("====== PARTICIPATE api response ois:  ", dataResp)
        return dataResp
    }
}