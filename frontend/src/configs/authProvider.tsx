import React from 'react'
import { useContext } from 'react';
import { useState, useEffect } from 'react';
import WalletConnect from "@walletconnect/client";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";

interface AuthProviderValue {
    currentAccount: string | null;
    setCurrentAccount: () => Promise<void> | null;
    disconnectAccount: () => void | null;
    apiToken: string | null,
    setApiToken: (addr: string | null) => Promise<void> | null,
}

const defVal: AuthProviderValue = {
    currentAccount: "" || null,
    setCurrentAccount: () => null,
    disconnectAccount: () => null,
    apiToken: null,
    setApiToken: () => null,
}

const AuthContext = React.createContext(defVal);

export const connector = new WalletConnect({
    bridge: "https://bridge.walletconnect.org", // Required
    qrcodeModal: QRCodeModal,
});

function AuthProvider(props: any) {
    const [currentAccount, setCurrentAccount] = useState<string>("")
    const [apiToken, setApiToken] = useState<string>("")

    const checkWalletIsConnected = async () => {

        if (connector.connected) {
            console.log("======= I'm already connected!");
            const { accounts } = connector;
            const address = accounts[0];
            setCurrentAccount(address);
            apiAuthTokenHandler(address)
        }
    }

    useEffect(() => {
        checkWalletIsConnected()
    }, [])

    const connectWalletHandler = async () => {
        if (!connector) {
            console.log("======== no connector. Please try again!")
            return
        }

        if (!connector.connected) {
            await connector.createSession();
        }
        connector.on("connect", (error, payload) => {
            if (error) {
                throw error;
            }
            const address = payload.params[0].accounts[0];
            setCurrentAccount(address);
        });
    }

    const disconnectWalletHandler = () => {
        connector.killSession()
        connector.on("disconnect", (error) => {

            if (error) {
                console.log("Disconnect Error: " + error)
                throw error;
            }
            setCurrentAccount("")
        });
    }

    const apiAuthTokenHandler = async (user_address: string | null) => {
        if (!user_address) {
            return
        }
        const b = {
            "user_address": user_address,
        }
        const res = await fetch('http://localhost:8080/user/auth', {
            method: 'POST',
            body: JSON.stringify(b),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await res.json();
        if (data && data.status) {
            setApiToken(data.token)
        }
    }

    return (
        <AuthContext.Provider value={{ currentAccount, setCurrentAccount: connectWalletHandler, disconnectAccount: disconnectWalletHandler, apiToken, setApiToken: apiAuthTokenHandler }}>{props.children}</AuthContext.Provider>
    );
}

function useAuth() {
    const authContext = useContext(AuthContext);
    return { ...authContext };
}

export { AuthProvider, useAuth };