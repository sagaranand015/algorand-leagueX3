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