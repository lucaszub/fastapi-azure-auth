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



export const createUser = async (userData: CreateUserRequest):Promise<void> => {
    try {
        await axios.post(getApiUrl('/auth/'), userData);
    } catch (error) {
        console.error("Error creating user", error);
        throw error;
    }
}
// export const createCustomer = async (customer: { nom: string; prenom:string; email: string; phone: string; address: string }) => {
//   try {
//     const response = await axios.post(getApiUrl('/customers/'), customer); // Route d'ajout
//     return response.data;
//   } catch (error) {
//     console.error("Error creating customer", error);
//     throw error;
//   }
// };
