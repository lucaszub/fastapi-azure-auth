import axios from 'axios';
import { getApiUrl } from '../config/api'; // Importer la fonction

export interface CreateUserRequest {
    username: string;
    password: string;
  }
  
  export interface TokenResponse {
    access_token: string;
    token_type: string;
  }
  export interface LoginRequest {
    username: string;
    password: string;
  }
  


export const createUser = async (userData: CreateUserRequest):Promise<void> => {
    try {
        await axios.post(getApiUrl('/auth/'), userData);
    } catch (error) {
        console.error("Error creating user", error);
        throw error;
    }
}


export const loginUser = async (loginData: LoginRequest) => {
  const response = await axios.post(getApiUrl('/auth/token'), 
    new URLSearchParams({
    username: loginData.username,
    password: loginData.password,
  }), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  }
);
  return response.data;
};


export const getCurrentUser = async (token: string): Promise<string> => {
  try {
      const response = await axios.get(getApiUrl('/auth/me'), {
          headers: {
              Authorization: `Bearer ${token}`,
          },
      });
      return response.data.message;
  } catch (error) {
      console.error("Error fetching user details", error);
      throw error;
  }
};
