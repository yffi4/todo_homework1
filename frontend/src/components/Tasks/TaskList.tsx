import React, { useState, useEffect } from "react";
import {
  List,
  ListItem,
  ListItemText,
  IconButton,
  Checkbox,
  Paper,
  Typography,
  Container,
  TextField,
  Button,
  Box,
  Tab,
  Tabs,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";
import TaskAnalytics from "../TaskAnalysis/TaskAnalytics";

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
}

interface TaskListProps {
  token: string;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`task-tabpanel-${index}`}
      aria-labelledby={`task-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const TaskList: React.FC<TaskListProps> = ({ token }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [tabValue, setTabValue] = useState(0);

  const fetchTasks = async () => {
    try {
      const response = await axios.get(process.env.REACT_APP_API_URL + "/api/tasks", {
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
        process.env.REACT_APP_API_URL + "/api/tasks",
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

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    try {
      await axios.patch(
        process.env.REACT_APP_API_URL + "/api/tasks/${taskId}",
        { completed: !completed },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      fetchTasks();
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await axios.delete(process.env.REACT_APP_API_URL + "/api/tasks/${taskId}", {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchTasks();
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ width: "100%", mt: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="task management tabs"
          >
            <Tab label="Tasks" />
            <Tab label="Analytics" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
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
                  <Checkbox
                    checked={task.completed}
                    onChange={() =>
                      handleToggleComplete(task.id, task.completed)
                    }
                  />
                  <ListItemText
                    primary={task.title}
                    secondary={task.description}
                  />
                
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={() => handleDeleteTask(task.id)}
                  sx={{ ml: "auto" }}
                >
                  <DeleteIcon />
                </IconButton>

                  
                </ListItem>
              ))}
            </List>
          </Paper>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <TaskAnalytics token={token} />
        </TabPanel>
      </Box>
    </Container>
  );
};

export default TaskList;
