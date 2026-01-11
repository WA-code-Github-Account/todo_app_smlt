// Vercel API function for getting tasks
import fs from 'fs';
import path from 'path';

const tasksFile = path.join(process.cwd(), 'todos.json');

export default function handler(req, res) {
  if (req.method === 'GET') {
    try {
      if (fs.existsSync(tasksFile)) {
        const data = fs.readFileSync(tasksFile, 'utf8');
        const tasks = JSON.parse(data);
        res.status(200).json(tasks);
      } else {
        res.status(200).json([]);
      }
    } catch (error) {
      res.status(500).json({ error: 'Failed to read tasks' });
    }
  } else if (req.method === 'POST') {
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