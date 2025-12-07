import { apiUrl } from '../../api/LoginService';
import msalInstance from './auth/AuthConfig';
import { io } from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 3;
  }

  async getAuthToken() {
    try {
      const accounts = msalInstance.getAllAccounts();
      if (accounts.length === 0) {
        throw new Error('No accounts found');
      }

      const tokenRequest = {
        scopes: ["User.Read"],
        account: accounts[0]
      };

      const response = await msalInstance.acquireTokenSilent(tokenRequest);
      return response.accessToken;
    } catch (error) {
      if (error.name === "InteractionRequiredAuthError") {
        const response = await msalInstance.acquireTokenPopup({
          scopes: ["User.Read"]
        });
        return response.accessToken;
      }
      throw error;
    }
  }

  async connect(fileId, onMessage) {
    if (this.socket) {
      await this.disconnect(fileId);
    }

    try {
      const token = await this.getAuthToken();

      // Fix the Socket.IO URL construction
      const socketUrl = apiUrl.replace(/\/$/, '');
      console.log('Connecting to Socket.IO server:', socketUrl);

      // Create Socket.IO connection
      this.socket = io(socketUrl, {
        transports: ['polling', 'websocket'],
        reconnection: true,
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 5000
      });

      // Connection event handlers
      this.socket.on('connect', () => {
        console.log('Socket.IO transport connected, authenticating...');

        // Send authentication after connection
        this.socket.emit('authenticate', {
          token: `Bearer ${token}`
        });
      });

      this.socket.on('auth_response', (response) => {
        console.log('Authentication response:', response);
        if (response.status === 'success') {
          this.reconnectAttempts = 0;
          // Only subscribe after successful authentication
          this.socket.emit('subscribe', { fileId });
        } else {
          console.error('Authentication failed:', response.message);
          this.disconnect(fileId);
        }
      });

      this.socket.on('connect_error', (error) => {
        console.error('Socket.IO connection error:', error);
        this.reconnectAttempts++;
      });

      this.socket.on('subscribe_response', (data) => {
        console.log('Subscription confirmed:', data);
      });

      this.socket.on('unsubscribe_response', (data) => {
        console.log('Unsubscription confirmed:', data);
      });

      this.socket.on('logs_update', (data) => {
        if (onMessage && (data.new_logs || data.updated_logs)) {
          // Pass both new and updated logs to the callback
          onMessage({
            newLogs: data.new_logs || [],
            updatedLogs: data.updated_logs || [],
            allLogs: data.all_logs || []  // Full state for sync
          });
        }
      });

      this.socket.on('error', (error) => {
        console.error('Socket.IO server error:', error);
      });

      this.socket.on('disconnect', (reason) => {
        console.log('Socket.IO disconnected:', reason);
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          this.disconnect(fileId);
        }
      });

      // Return a proper cleanup function that can be called by React's useEffect
      const cleanup = () => {
        console.log('Cleanup function called for fileId:', fileId);
        return this.disconnect(fileId);
      };

      return cleanup;  // Return the cleanup function directly
    } catch (error) {
      console.error('Error establishing Socket.IO connection:', error);
      // Return a no-op cleanup function in case of error
      return () => { };
    }
  }

  async disconnect(fileId) {
    if (this.socket) {
      try {
        console.log('Disconnecting WebSocket for fileId:', fileId);

        // Only try to unsubscribe if we have a fileId and the socket is connected
        if (fileId && this.socket.connected) {
          console.log('Unsubscribing from updates...');
          this.socket.emit('unsubscribe', { fileId });

          // Wait for unsubscribe confirmation or timeout
          await new Promise((resolve) => {
            const timeout = setTimeout(() => {
              console.log('Unsubscribe timeout - proceeding with disconnect');
              resolve();
            }, 1000);

            this.socket.once('unsubscribe_response', (response) => {
              console.log('Unsubscribe response:', response);
              clearTimeout(timeout);
              resolve();
            });
          });
        }

        // Disconnect the socket
        if (this.socket.connected) {
          this.socket.disconnect();
        }
      } catch (error) {
        console.error('Error disconnecting Socket.IO:', error);
      }
      this.socket = null;
    }
    this.reconnectAttempts = 0;
  }
}

export default new WebSocketService(); 