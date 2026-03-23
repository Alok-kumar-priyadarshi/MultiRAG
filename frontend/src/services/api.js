import axios from "axios";


const API = axios.create({
  baseURL: import.meta.env.REACT_APP_API_BASE_URL,
});

export const sendMessage = async ({ query, url, file, session_id }) => {
  const formData = new FormData();

  if (query) formData.append("query", query);
  if (url) formData.append("url", url);
  if (file) formData.append("file", file);
  formData.append("session_id", session_id);

  const response = await API.post("/chat", formData);
  return response.data;
};

export const resetChat = async () => {
  await API.post("/reset");
};
