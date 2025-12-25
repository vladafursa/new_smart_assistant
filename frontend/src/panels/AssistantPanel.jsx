import SummaryBox from '../components/Summary.jsx';
import Form from '../components/Form.jsx';
import { useState } from "react";

const AssistantPanel = ({ summary_text, onSend}) => {
  return (
    <div className="flex flex-col h-full">
     
      <SummaryBox text={summary_text} />

      <div className="mt-auto">
          <Form sender="assistant" onSend={(text) => onSend(text, "assistant")} />
      </div>
    </div>
  );
};

export default AssistantPanel;