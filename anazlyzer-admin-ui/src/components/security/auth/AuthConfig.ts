import { PublicClientApplication, LogLevel, Configuration } from "@azure/msal-browser";

// Define the MSAL configuration with proper types
const msalConfig: Configuration = {
  auth: {
    clientId: import.meta.env.VITE_AZURE_CLIENT_ID,
    authority: import.meta.env.VITE_AZURE_AUTHORITY,
    redirectUri: import.meta.env.VITE_REDIRECT_URI,
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false,
  },
  system: {
    loggerOptions: {
      loggerCallback: (level: LogLevel, message: string, containsPii: boolean) => {
        if (containsPii) {
          return;
        }
        switch (level) {
          case LogLevel.Error:
            console.error(message);
            return;
          case LogLevel.Info:
            console.info(message);
            return;
          case LogLevel.Verbose:
            console.debug(message);
            return;
          case LogLevel.Warning:
            console.warn(message);
            return;
          default:
            return;
        }
      }
    }
  }
};

// Create the MSAL instance
const msalInstance = new PublicClientApplication(msalConfig);

// Initialize MSAL and handle redirect
export const initializeMsal = async (): Promise<unknown> => {
  try {
    // First initialize MSAL
    await msalInstance.initialize();

    // Then handle redirect
    const result = await msalInstance.handleRedirectPromise();
    return result;
  } catch (error) {
    console.error('MSAL initialization error:', error);
    throw error;
  }
};

// Keep track of initialization state
let isInitialized = false;

// Wrapper function to ensure MSAL is initialized before use
export const getMsalInstance = async (): Promise<PublicClientApplication> => {
  if (!isInitialized) {
    await msalInstance.initialize();
    isInitialized = true;
  }
  return msalInstance;
};

export default msalInstance;