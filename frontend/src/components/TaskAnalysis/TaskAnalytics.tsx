import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  Button,
  Alert,
} from "@mui/material";
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from "@mui/lab";
import axios from "axios";

interface TaskAnalyticsProps {
  token: string;
}

interface TaskAnalysis {
  summary: {
    task_distribution: {
      total_tasks: number;
      completed_tasks: number;
      pending_tasks: number;
      completion_rate: number;
    };
    workload_status: string;
    optimization_tips: string[];
  };
  priority_tasks: Array<{
    id: number;
    title: string;
    reason: string;
  }>;
  individual_analyses: Array<{
    task_id: number;
    analysis: string;
    success: boolean;
  }>;
}

const TaskAnalytics: React.FC<TaskAnalyticsProps> = ({ token }) => {
  const [analysis, setAnalysis] = useState<TaskAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        process.env.REACT_APP_API_URL + "/api/tasks/analyze",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setAnalysis(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch task analysis");
      console.error("Error fetching analysis:", err);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchAnalysis();
  }, [token, fetchAnalysis]);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="200px"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!analysis) {
    return <Alert severity="info">No analysis available</Alert>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Task Analysis Dashboard
      </Typography>

      {/* Task Distribution Card */}
      <div className="grid gap-3 grid-cols-1 md:grid-cols-2">
        <div>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Task Distribution
              </Typography>
              <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
                <Chip
                  label={`Total: ${analysis.summary.task_distribution.total_tasks}`}
                  color="primary"
                />
                <Chip
                  label={`Completed: ${analysis.summary.task_distribution.completed_tasks}`}
                  color="success"
                />
                <Chip
                  label={`Pending: ${analysis.summary.task_distribution.pending_tasks}`}
                  color="warning"
                />
              </Box>
              <Typography variant="body1">
                Completion Rate:{" "}
                {analysis.summary.task_distribution.completion_rate.toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </div>

        {/* Workload Status Card */}
        <div>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Workload Status
              </Typography>
              <Typography variant="body1" color="text.secondary">
                {analysis.summary.workload_status}
              </Typography>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Priority Tasks */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Priority Tasks
          </Typography>
          <Timeline>
            {analysis.priority_tasks.map((task) => (
              <TimelineItem key={task.id}>
                <TimelineSeparator>
                  <TimelineDot color="primary" />
                  <TimelineConnector />
                </TimelineSeparator>
                <TimelineContent>
                  <Typography variant="subtitle1">{task.title}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {task.reason}
                  </Typography>
                </TimelineContent>
              </TimelineItem>
            ))}
          </Timeline>
        </CardContent>
      </Card>

      {/* Optimization Tips */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Optimization Tips
          </Typography>
          <List>
            {analysis.summary.optimization_tips.map((tip, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemText primary={tip} />
                </ListItem>
                {index < analysis.summary.optimization_tips.length - 1 && (
                  <Divider />
                )}
              </React.Fragment>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Individual Task Analyses */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Detailed Task Analysis
          </Typography>
          <List>
            {analysis.individual_analyses.map((item, index) => (
              <React.Fragment key={item.task_id}>
                <ListItem>
                  <ListItemText
                    primary={`Task #${item.task_id}`}
                    secondary={item.analysis}
                  />
                </ListItem>
                {index < analysis.individual_analyses.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </CardContent>
      </Card>

      <Box sx={{ mt: 3, display: "flex", justifyContent: "center" }}>
        <Button variant="contained" color="primary" onClick={fetchAnalysis}>
          Refresh Analysis
        </Button>
      </Box>
    </Box>
  );
};

export default TaskAnalytics;
