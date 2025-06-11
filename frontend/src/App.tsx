import React, { useState } from "react";
import { Container, Box, Tab, Tabs } from "@mui/material";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import TaskList from "./components/Tasks/TaskList";

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [authTab, setAuthTab] = useState(0);

  const handleLogin = (newToken: string) => {
    setToken(newToken);
  };

  const handleRegisterSuccess = () => {
    setAuthTab(0); // Switch to login tab after successful registration
  };

  if (!token) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ width: "100%", mt: 4 }}>
          <Tabs
            value={authTab}
            onChange={(_, newValue) => setAuthTab(newValue)}
            centered
          >
            <Tab label="Login" />
            <Tab label="Register" />
          </Tabs>
          <Box sx={{ mt: 2 }}>
            {authTab === 0 ? (
              <Login onLogin={handleLogin} />
            ) : (
              <Register onRegisterSuccess={handleRegisterSuccess} />
            )}
          </Box>
        </Box>
      </Container>
    );
  }

  return <TaskList token={token} />;
}

export default App;
