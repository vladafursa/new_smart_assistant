import { useEffect, useState } from "react";

const FileList = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await fetch("http://localhost:8000/files");
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to fetch files");
        }

        setFiles(data.files);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  if (loading) return <p className="text-blue-500">Loading files...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
    <div className="w-full mt-6">
      <h2 className="text-lg font-semibold mb-4">Uploaded Files</h2>
      <ul className="space-y-2">
        {files.map((f) => (
          <li key={f.filename} className="flex justify-between items-center p-2 border rounded">
            <span>{f.filename}</span>
            <a
              href={f.preview_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Preview
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileList;
