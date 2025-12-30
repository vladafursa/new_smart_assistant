import Header from "../components/Header.jsx";
import AssistantPanel from "../panels/AssistantPanel.jsx";
import UserPanel from "../panels/UserPanel.jsx";
import { useState } from "react";

const Home = () => {
  const [chatMessages, setChatMessages] = useState([
    { sender: "assistant", message: "Hello! How can I help you?" },
  ]);

  const [assistantResponse, setAssistantResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSend = async (text, sender) => {
    setChatMessages((prev) => [...prev, { sender, message: text }]);

    if (sender === "user") {
      setLoading(true);
      setErrorMsg("");

      try {
        const res = await fetch("http://localhost:8000/rag", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: text }),
        });

        if (!res.ok) {
          throw new Error(`Bad response: ${res.status}`);
        }

        const data = await res.json();

        setAssistantResponse(data);
      } catch (err) {
        console.error(err);
        setErrorMsg("Smth went wrong. Try again.");
      } finally {
        setLoading(false);
      }
    }
  };

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
            summary_text={
              loading
                ? "Loading answers…"
                : assistantResponse?.answer || "There will be summary"
            }
            chunks={assistantResponse?.chunks || []}
            errorMsg={errorMsg}
            onSend={handleSend}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
