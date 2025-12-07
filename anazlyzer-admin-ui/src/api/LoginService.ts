import axios from 'axios';
import msalInstance from "../components/security/auth/AuthConfig";
import { InteractionRequiredAuthError } from "@azure/msal-browser";

// Set base URL from environment variables
console.log('Base URL:', import.meta.env.VITE_SPOKE_API_BASE_URL);
export const apiUrl = import.meta.env.VITE_SPOKE_API_BASE_URL;

const api = axios.create({
    baseURL: apiUrl,
});

// Secure function to get authentication token using MSAL
const getAuthToken = async () => {
    try {
        const accounts = msalInstance.getAllAccounts();
        if (accounts.length === 0) {
            throw new Error('No accounts found. User needs to sign in.');
        }

        const tokenRequest = {
            scopes: ["User.Read"],  // Adjust scopes based on your API requirements
            account: accounts[0]
        };

        console.log(tokenRequest)
        const response = await msalInstance.acquireTokenSilent(tokenRequest);
        return response.accessToken ? `Bearer ${response.accessToken}` : null;  // Use accessToken
    } catch (error) {
        if (error instanceof InteractionRequiredAuthError) {
            try {
                const response = await msalInstance.acquireTokenPopup({
                    scopes: ["User.Read"]
                });
                return response.accessToken ? `Bearer ${response.accessToken}` : null;
            } catch (interactiveError) {
                console.error('Error during interactive token acquisition:', interactiveError);
                throw new Error('Interactive token acquisition failed');
            }
        }
        console.error('Error acquiring token:', error);
        throw new Error('Token acquisition failed');
    }
};


// Request interceptor to add API key or MSAL token to headers
api.interceptors.request.use(
    async (config) => {
        try {
            // Check if API key is provided in the config
            const apiKey = config.apiKey || localStorage.getItem('api_key');
            if (apiKey) {
                // Always ensure apiKey is securely stored (in backend or secure storage)
                config.headers.Authorization = `ApiKey ${apiKey}`;
                return config;
            }

            // Fall back to MSAL token if API key is not provided
            const token = await getAuthToken();
            if (token) {
                config.headers.Authorization = token;
            }
            return config;
        } catch (error) {
            console.error('Error in request interceptor:', error);
            return Promise.reject(new Error('Request interceptor failed'));
        }
    },
    (error) => Promise.reject(error)
);

// Request wrapper to handle GET requests with improved error handling
export const getRequest = async <T = unknown>(endpoint: string) => {
    try {
        const response = await api.get<T>(endpoint);
        return response.data;
    } catch (error) {
        console.error(`Error fetching data from ${endpoint}:`, error);
        throw new Error(`Failed to fetch data from ${endpoint}`);
    }
};

export const fetchUserInfo = () => getRequest('/app/v1/auth/user/userinfo');