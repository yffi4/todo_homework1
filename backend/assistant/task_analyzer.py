from typing import List, Dict
import openai 
from models import Task
import os
from dotenv import load_dotenv

load_dotenv()

class TaskAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def analyze_task(self, task: Task) -> Dict:
        """
        Analyze a single task and provide insights
        """
        prompt = f"""
        Analyze this task and provide recommendations:
        Title: {task.title}
        Description: {task.description}
        Status: {"Completed" if task.completed else "Not Completed"}

        Provide:
        1. Priority Level (High/Medium/Low)
        2. Estimated time to complete
        3. Suggested deadline
        4. Any potential dependencies or prerequisites
        5. Tips for efficient completion
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that analyzes tasks and provides practical recommendations."},
                    {"role": "user", "content": prompt}
                ]
            )

            analysis = response.choices[0].message.content
            return {
                "task_id": task.id,
                "analysis": analysis,
                "success": True
            }

        except Exception as e:
            print(f"Error analyzing task: {e}")
            return {
                "task_id": task.id,
                "analysis": "Error occurred during analysis",
                "success": False
            }

    def get_task_distribution(self, tasks: List[Task]) -> Dict:
        """
        Get distribution of tasks by completion status and analyze workload
        """
        total_tasks = len(tasks)
        completed_tasks = len([task for task in tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }

    def get_workload_analysis(self, tasks: List[Task]) -> Dict:
        """
        Analyze workload and provide recommendations for task management
        """
        distribution = self.get_task_distribution(tasks)
        pending_tasks = [task for task in tasks if not task.completed]

        recommendations = {
            "workload_status": self._get_workload_status(distribution),
            "priority_tasks": self._identify_priority_tasks(pending_tasks),
            "optimization_tips": self._generate_optimization_tips(distribution, pending_tasks)
        }

        return recommendations

    def _get_workload_status(self, distribution: Dict) -> str:
        """
        Determine workload status based on task distribution
        """
        completion_rate = distribution["completion_rate"]
        pending_tasks = distribution["pending_tasks"]

        if completion_rate >= 80:
            return "Excellent progress! Keep up the good work."
        elif completion_rate >= 50:
            return "Good progress, but there's room for improvement."
        elif pending_tasks > 10:
            return "High workload detected. Consider prioritizing or delegating tasks."
        else:
            return "Moderate workload. Focus on completing high-priority tasks first."

    def _identify_priority_tasks(self, tasks: List[Task], limit: int = 5) -> List[Dict]:
        """
        Identify top priority tasks that need attention
        """
        # In a real implementation, you might want to use more sophisticated
        # priority calculation based on due dates, dependencies, etc.
        return [
            {
                "id": task.id,
                "title": task.title,
                "reason": "Pending task requiring attention"
            }
            for task in tasks[:limit]
        ]

    def _generate_optimization_tips(self, distribution: Dict, pending_tasks: List[Task]) -> List[str]:
        """
        Generate specific tips for optimizing task completion
        """
        tips = []
        
        if distribution["pending_tasks"] > 5:
            tips.append("Consider breaking down larger tasks into smaller, manageable subtasks.")
            
        if distribution["completion_rate"] < 50:
            tips.append("Try using time-blocking techniques to focus on one task at a time.")
            
        if len(pending_tasks) > 10:
            tips.append("Review and reprioritize tasks to ensure you're focusing on the most important ones.")
            
        if distribution["completed_tasks"] == 0:
            tips.append("Start with the easiest task to build momentum.")
            
        tips.append("Regular breaks can help maintain productivity and focus.")
        
        return tips

    def batch_analyze_tasks(self, tasks: List[Task]) -> Dict:
        """
        Provide comprehensive analysis for a batch of tasks
        """
        individual_analyses = []
        for task in tasks:
            analysis = self.analyze_task(task)
            if analysis["success"]:
                individual_analyses.append(analysis)

        workload_analysis = self.get_workload_analysis(tasks)
        distribution = self.get_task_distribution(tasks)

        return {
            "summary": {
                "task_distribution": distribution,
                "workload_status": workload_analysis["workload_status"],
                "optimization_tips": workload_analysis["optimization_tips"]
            },
            "priority_tasks": workload_analysis["priority_tasks"],
            "individual_analyses": individual_analyses
        } 