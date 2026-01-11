// Vercel API function for all task operations
import fs from 'fs';
import path from 'path';

const tasksFile = path.join(process.cwd(), 'todos.json');

export default function handler(req, res) {
  const { method } = req;
  const { id } = req.query;

  if (method === 'GET') {
    // Get all tasks or a specific task
    try {
      if (fs.existsSync(tasksFile)) {
        const data = fs.readFileSync(tasksFile, 'utf8');
        const tasks = JSON.parse(data);
        
        if (id) {
          // Get specific task
          const taskId = parseInt(id);
          const task = tasks.find(t => t.id === taskId);
          
          if (task) {
            res.status(200).json(task);
          } else {
            res.status(404).json({ error: 'Task not found' });
          }
        } else {
          // Get all tasks
          res.status(200).json(tasks);
        }
      } else {
        res.status(200).json([]);
      }
    } catch (error) {
      res.status(500).json({ error: 'Failed to read tasks' });
    }
  } else if (method === 'POST') {
    // Add new task
    try {
      const { title, description } = req.body;
      
      if (!title) {
        return res.status(400).json({ error: 'Title is required' });
      }

      let tasks = [];
      if (fs.existsSync(tasksFile)) {
        const data = fs.readFileSync(tasksFile, 'utf8');
        tasks = JSON.parse(data);
      }

      const newTask = {
        id: Math.max(...tasks.map(t => t.id), 0) + 1 || 1,
        title,
        description: description || '',
        status: 'incomplete',
        createdAt: new Date().toISOString()
      };

      tasks.push(newTask);
      
      fs.writeFileSync(tasksFile, JSON.stringify(tasks, null, 2));
      
      res.status(200).json(newTask);
    } catch (error) {
      res.status(500).json({ error: 'Failed to add task' });
    }
  } else if (method === 'PUT' && id) {
    // Toggle task status
    try {
      const taskId = parseInt(id);
      
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
  } else if (method === 'DELETE' && id) {
    // Delete task
    try {
      const taskId = parseInt(id);
      
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

export const config = {
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
};