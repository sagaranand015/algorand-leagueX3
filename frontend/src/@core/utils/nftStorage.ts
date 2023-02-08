import { NFTStorage } from 'nft.storage';
import { NFT_STORAGE_KEY } from './constants';

export function GetStorageClient() {
    const client = new NFTStorage({ token: NFT_STORAGE_KEY });
    return client;
}

export function FetchDataFromIpfsLink(cid: string) {
    if (cid.startsWith('ipfs')) {
        cid = cid.replace('ipfs://', 'https://ipfs.io/ipfs/')
        console.log("cid is:  ", cid);
        return cid
    } else {
        const url = `https://ipfs.io/ipfs/${cid}`;
        console.log("final link from ipfs: ", url);
        return url
    }
}

export async function UploadNftJson(name: string, description: string, release: string, director: string, image: string, metadata: string) {
    const client = GetStorageClient();
    const data = {
        "name": name,
        "description": description,
        "image": image,
        "release": release,
        "director": director,
        "metadata": metadata,
    }
    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    return await client.storeBlob(blob);
}

export async function GetLeagueDataIpfsLink(league_data: any) {
    const client = GetStorageClient();
    const blob = new Blob([JSON.stringify(league_data)], { type: 'application/json' });
    console.log("======== storing leagues data", blob)
    return await client.storeBlob(blob);
}

export async function GetSquadDataIpfsLink(squad_data: any) {
    const client = GetStorageClient();
    const blob = new Blob([JSON.stringify(squad_data)], { type: 'application/json' });
    console.log("======== storing squads data", blob)
    return await client.storeBlob(blob);
}