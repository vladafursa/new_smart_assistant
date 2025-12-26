import Header from "../components/Header.jsx";
import AssistantPanel from "../panels/AssistantPanel.jsx";
import UserPanel from "../panels/UserPanel.jsx";
import { useState } from "react";

const Home = () => {
  const [chatMessages, setChatMessages] = useState([
    { sender: "assistant", message: "Hello! How can I help you?" },
  ]);

  const handleSend = (text, sender) => {
    setChatMessages((prev) => [...prev, { sender, message: text }]);
  };

  const summaryText = "There will be summary";
  return (
    <div className="h-screen flex flex-col bg-neutral-50">
      <div className="sticky top-0">
        <Header />
      </div>
      <div className="flex flex-1">
        <div className="flex-[0.4] border-r p-4">
          <UserPanel chatMessages={chatMessages} onSend={handleSend} />
        </div>

        <div className="flex-[0.6] p-4">
          <AssistantPanel
            summary_text={summaryText}
            chatMessages={chatMessages}
            onSend={handleSend}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
