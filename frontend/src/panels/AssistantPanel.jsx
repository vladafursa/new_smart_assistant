import SummaryBox from "../components/Summary.jsx";
import Form from "../components/Form.jsx";

const AssistantPanel = ({ summary_text, chunks, errorMsg, onSend }) => {
  return (
    <div className="flex flex-col h-full">
      <SummaryBox text={summary_text} />

      {errorMsg && (
        <div className="p-3 my-2 rounded bg-red-50 text-red-700 border border-red-200">
          {errorMsg}
        </div>
      )}

      <div className="p-4 space-y-3">
        {chunks.length > 0 ? (
          chunks.map((chunk, i) => (
            <div key={i} className="border p-3 rounded">
              <p className="mb-1">
                <strong>Q:</strong> {chunk.text}
              </p>
              <p className="text-sm text-gray-600">
                <strong>Source:</strong> {chunk.source}
              </p>
              <p className="text-sm text-gray-600">
                <strong>Category:</strong> {chunk.category}
              </p>
            </div>
          ))
        ) : (
          <p className="text-sm text-gray-500">
            Здесь появятся релевантные куски (chunks) после запроса.
          </p>
        )}
      </div>

      <div className="mt-auto">
        <Form sender="assistant" onSend={(text) => onSend(text, "assistant")} />
      </div>
    </div>
  );
};

export default AssistantPanel;
