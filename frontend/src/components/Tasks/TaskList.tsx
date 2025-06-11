import React, { useState, useEffect } from "react";
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Checkbox,
  Paper,
  Typography,
  Container,
  TextField,
  Button,
  Box,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
}

interface TaskListProps {
  token: string;
}

const TaskList: React.FC<TaskListProps> = ({ token }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");

  const fetchTasks = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/tasks", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [token]);

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(
        "http://localhost:8000/api/tasks",
        {
          title: newTaskTitle,
          description: newTaskDescription,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setNewTaskTitle("");
      setNewTaskDescription("");
      fetchTasks();
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Tasks
        </Typography>

        <Paper sx={{ p: 2, mb: 2 }}>
          <form onSubmit={handleAddTask}>
            <TextField
              fullWidth
              label="Task Title"
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Task Description"
              value={newTaskDescription}
              onChange={(e) => setNewTaskDescription(e.target.value)}
              margin="normal"
              multiline
              rows={2}
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              sx={{ mt: 2 }}
            >
              Add Task
            </Button>
          </form>
        </Paper>

        <Paper>
          <List>
            {tasks.map((task) => (
              <ListItem key={task.id} divider>
                <Checkbox checked={task.completed} />
                <ListItemText
                  primary={task.title}
                  secondary={task.description}
                />
                <ListItemSecondaryAction>
                  <IconButton edge="end" aria-label="delete">
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
    </Container>
  );
};

export default TaskList;
