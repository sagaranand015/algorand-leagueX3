import React from 'react'
import { useContext } from 'react';
import { useState, useEffect } from 'react';
import WalletConnect from "@walletconnect/client";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";

interface AuthProviderValue {
    currentAccount: string | null;
    setCurrentAccount: () => Promise<void> | null;
    disconnectAccount: () => void | null;
}

const defVal: AuthProviderValue = {
    currentAccount: "" || null,
    setCurrentAccount: () => null,
    disconnectAccount: () => null
}

const AuthContext = React.createContext(defVal);

export const connector = new WalletConnect({
    bridge: "https://bridge.walletconnect.org", // Required
    qrcodeModal: QRCodeModal,
});

function AuthProvider(props: any) {
    const [currentAccount, setCurrentAccount] = useState<string>("")

    const checkWalletIsConnected = async () => {

        if (connector.connected) {
            console.log("======= I'm already connected!");
            const { accounts } = connector;
            const address = accounts[0];
            setCurrentAccount(address);
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

    return (
        <AuthContext.Provider value={{ currentAccount, setCurrentAccount: connectWalletHandler, disconnectAccount: disconnectWalletHandler }}>{props.children}</AuthContext.Provider>
    );
}

function useAuth() {
    const authContext = useContext(AuthContext);
    return { ...authContext };
}

export { AuthProvider, useAuth };