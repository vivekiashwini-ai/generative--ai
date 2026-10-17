const conversation = document.querySelector('#conversation');
const chatForm = document.querySelector('#chat-form');
const messageInput = document.querySelector('#message-input');
const sendButton = document.querySelector('#send-button');
const profileDialog = document.querySelector('#profile-dialog');
const profileForm = document.querySelector('#profile-form');
const connectionStatus = document.querySelector('#connection-status');
const statusDot = document.querySelector('#status-dot');
const history = [];
const profileDefaults = {
  name: 'friend',
  interests: 'general topics',
  experience: 'not specified',
  style: 'friendly and clear',
};

let profile = loadProfile();

function loadProfile() {
  try {
    return { ...profileDefaults, ...JSON.parse(localStorage.getItem('mira-profile') || '{}') };
  } catch {
    return { ...profileDefaults };
  }
}

function saveProfile() {
  localStorage.setItem('mira-profile', JSON.stringify(profile));
  document.querySelector('#profile-name').textContent = profile.name;
  document.querySelector('#profile-avatar').textContent = (profile.name.trim()[0] || 'F').toUpperCase();
  document.querySelector('#profile-detail').textContent = profile.interests || 'Getting to know you';
  document.querySelector('#welcome-message').textContent = `Hi, ${profile.name}. What would you like to talk about?`;
}

function addMessage(role, text, details = {}) {
  const article = document.createElement('article');
  article.className = `message ${role === 'user' ? 'user-message' : 'assistant-message'}`;

  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.setAttribute('aria-hidden', 'true');
  avatar.textContent = role === 'user' ? (profile.name.trim()[0] || 'F').toUpperCase() : 'M';

  const body = document.createElement('div');
  body.className = 'message-body';
  const meta = document.createElement('div');
  meta.className = 'message-meta';
  const sender = document.createElement('strong');
  sender.textContent = role === 'user' ? profile.name : 'Mira';
  const time = document.createElement('time');
  time.textContent = new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  meta.append(sender, time);

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  body.append(meta, bubble);

  if (details.emotion) {
    const emotion = document.createElement('div');
    emotion.className = 'emotion-label';
    emotion.textContent = `Possible tone: ${details.emotion} (${details.confidence || 'low'} confidence)`;
    body.append(emotion);
  }

  article.append(avatar, body);
  conversation.append(article);
  conversation.scrollTop = conversation.scrollHeight;
  return article;
}

function setConnection(text, state) {
  connectionStatus.textContent = text;
  statusDot.className = `status-dot ${state || ''}`;
}

async function checkHealth() {
  try {
    const response = await fetch('/api/health');
    const result = await response.json();
    if (!response.ok) throw new Error('Server is not responding');
    setConnection(result.llmConfigured ? 'Ready to chat' : 'Server ready · API key needed', result.llmConfigured ? 'ready' : '');
  } catch {
    setConnection('Backend unavailable', 'error');
  }
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message || sendButton.disabled) return;

  addMessage('user', message);
  messageInput.value = '';
  sendButton.disabled = true;
  sendButton.querySelector('span:first-child').textContent = 'Thinking';
  const typing = addMessage('assistant', 'Putting my thoughts together...');
  typing.classList.add('typing');

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history, profile }),
    });
    const result = await response.json();
    typing.remove();
    if (!response.ok) throw new Error(result.error || 'The request could not be completed.');

    history.push({ role: 'user', content: message }, { role: 'assistant', content: result.reply });
    if (history.length > 12) history.splice(0, history.length - 12);
    addMessage('assistant', result.reply, { emotion: result.emotion, confidence: result.confidence });
  } catch (error) {
    typing.remove();
    addMessage('assistant', error.message);
  } finally {
    sendButton.disabled = false;
    sendButton.querySelector('span:first-child').textContent = 'Send';
    messageInput.focus();
  }
});

messageInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

document.querySelector('#clear-chat').addEventListener('click', () => {
  history.length = 0;
  conversation.replaceChildren();
  const divider = document.createElement('div');
  divider.className = 'day-divider';
  const label = document.createElement('span');
  label.textContent = 'Today';
  divider.append(label);
  conversation.append(divider);
  addMessage('assistant', `Hi, ${profile.name}. What would you like to talk about?`);
  messageInput.focus();
});

document.querySelector('#open-profile').addEventListener('click', () => {
  for (const [key, value] of Object.entries(profile)) {
    const field = profileForm.elements.namedItem(key);
    if (field) field.value = value;
  }
  profileDialog.showModal();
});

profileForm.addEventListener('submit', (event) => {
  event.preventDefault();
  profile = Object.fromEntries(new FormData(profileForm).entries());
  saveProfile();
  profileDialog.close();
});

document.querySelector('#close-profile').addEventListener('click', () => profileDialog.close());
document.querySelector('#cancel-profile').addEventListener('click', () => profileDialog.close());
saveProfile();
checkHealth();
