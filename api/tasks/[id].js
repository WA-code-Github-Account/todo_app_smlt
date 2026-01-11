// Vercel API function for toggling/deleting tasks
import fs from 'fs';
import path from 'path';

const tasksFile = path.join(process.cwd(), 'todos.json');

export default function handler(req, res) {
  const { id } = req.query;
  const taskId = parseInt(id);

  if (isNaN(taskId)) {
    return res.status(400).json({ error: 'Invalid task ID' });
  }

  if (req.method === 'PUT') {
    // Toggle task status
    try {
      if (!fs.existsSync(tasksFile)) {
        return res.status(404).json({ error: 'Tasks file not found' });
      }

      let tasks = JSON.parse(fs.readFileSync(tasksFile, 'utf8'));
      const taskIndex = tasks.findIndex(t => t.id === taskId);

      if (taskIndex === -1) {
        return res.status(404).json({ error: 'Task not found' });
      }

      tasks[taskIndex].status = tasks[taskIndex].status === 'complete' ? 'incomplete' : 'complete';
      
      fs.writeFileSync(tasksFile, JSON.stringify(tasks, null, 2));
      
      res.status(200).json(tasks[taskIndex]);
    } catch (error) {
      res.status(500).json({ error: 'Failed to toggle task' });
    }
  } else if (req.method === 'DELETE') {
    // Delete task
    try {
      if (!fs.existsSync(tasksFile)) {
        return res.status(404).json({ error: 'Tasks file not found' });
      }

      let tasks = JSON.parse(fs.readFileSync(tasksFile, 'utf8'));
      const filteredTasks = tasks.filter(t => t.id !== taskId);

      if (filteredTasks.length === tasks.length) {
        return res.status(404).json({ error: 'Task not found' });
      }

      fs.writeFileSync(tasksFile, JSON.stringify(filteredTasks, null, 2));
      
      res.status(200).json({ message: 'Task deleted successfully' });
    } catch (error) {
      res.status(500).json({ error: 'Failed to delete task' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}