// server/src/index.js
import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import cors from 'cors';

const app = express();
app.use(express.json());
app.use(cors());

// 기본 라우트
app.get('/ping', (req, res) => {
  res.send('pong');
});

// 에이전트 설정 요청 API
app.get('/api/config/:agentId', (req, res) => {
  const { agentId } = req.params;
  // 추후 DB 연결, 지금은 mock 응답
  res.json({
    agentId,
    config: {
      scanInterval: 60,
      logging: true,
    },
  });
});

// 에이전트 로그 수신 API
app.post('/api/logs', (req, res) => {
  const log = req.body;
  console.log('Log received:', log);
  res.status(200).json({ status: 'ok' });
});

// React 빌드된 웹 서빙
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// const distPath = path.join(__dirname, '../../web/dist');
// app.use(express.static(distPath));
// app.get('*', (req, res) => {
//   res.sendFile(path.join(distPath, 'index.html'));
// });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ nacfy server running on http://localhost:${PORT}`));
