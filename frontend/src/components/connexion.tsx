import React, { useState, useEffect } from 'react';
import classNames from 'classnames';
import { loginUser, LoginRequest } from '../service/authservice';
import { getCurrentUser } from '../service/authservice'; // Assure-toi que cette fonction est exportée de ton service
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from './ui/button';

export function Connexion({
  className,
  ...props
}: React.ComponentPropsWithoutRef<"div">) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null); // Token type can either be a string or null
  const [userGreeting, setUserGreeting] = useState<string | null>(null); // Pour afficher le message de bienvenue

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    const loginData: LoginRequest = { username, password };
    try {
      const response = await loginUser(loginData);
      setToken(response.access_token); // Store token if needed (e.g., in localStorage or context)
      setMessage('Login successful');

      // Récupérer les informations de l'utilisateur après la connexion
      if (response.access_token) {
        const greetingMessage = await getCurrentUser(response.access_token);
        setUserGreeting(`Hello ${greetingMessage}, vous êtes connecté.`);
      }

    } catch (error) {
      setMessage('Error logging in');
      console.error('Error logging in:', error);
    }
  };

  // Optionnellement, on peut afficher un message si un token est déjà présent.
  useEffect(() => {
    if (token) {
      getCurrentUser(token).then(greetingMessage => {
        setUserGreeting(`Hello ${greetingMessage}, vous êtes connecté.`);
      });
    }
  }, [token]);

  return (
    <div className={classNames("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Login</CardTitle>
          <CardDescription>
            Enter your username and password to login
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <Button type="submit" className="btn btn-primary">
                Login
              </Button>
              {message && (
                <div className="mt-4 text-center">
                  <p>{message}</p>
                </div>
              )}
              {userGreeting && (
                <div className="mt-4 text-center text-green-500">
                  <p>{userGreeting}</p>
                </div>
              )}
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
