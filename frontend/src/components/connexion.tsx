import React, { useState } from 'react';
import classNames from 'classnames';
import { loginUser, LoginRequest } from '../service/authservice';
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

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    const loginData: LoginRequest = { username, password };
    try {
      const response = await loginUser(loginData);
      setToken(response.access_token); // Store token if needed (e.g., in localStorage or context)
      setMessage('Login successful');
      console.log("Token: " + token)
    } catch (error) {
      setMessage('Error logging in');
      console.error('Error logging in:', error);
    }
  }; // handleLogin

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
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
