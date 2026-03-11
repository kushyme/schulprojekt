import { useState, useEffect, useCallback } from "react";
import "./App.css";

type CatImage = {
  id: string;
  url: string;
  breeds?: { id: string; name: string }[];
}

type Breed = {
  id: string;
  name: string;
}

const API_KEY = "mabey später";
const BASE_URL = "https://api.thecatapi.com/v1";

const get = (path: string) =>
  fetch(`${BASE_URL}${path}`, {
    headers: { "x-api-key": API_KEY },
  }).then((r) => r.json());

export default function App() {
  const [cats, setCats] = useState<CatImage[]>([]);
  const [breeds, setBreeds] = useState<Breed[]>([]);
  const [selectedBreed, setSelectedBreed] = useState("");
  const [limitMode, setLimitMode] = useState<"all" | "custom">("custom");
  const [customLimit, setCustomLimit] = useState(9);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    get("/breeds?limit=100").then((data: Breed[]) => {
      if (Array.isArray(data)) setBreeds(data);
    });
  }, []);

  const fetchCats = useCallback(async () => {
    setLoading(true);
    setCats([]);
    try {
      if (limitMode === "all") {
        const pages = await Promise.all(
          [0, 1, 2, 3, 4].map((page) =>
            get(
              `/images/search?limit=100&page=${page}&order=RAND${
                selectedBreed ? `&breed_ids=${selectedBreed}` : ""
              }`
            )
          )
        );
        setCats(pages.flat());
      } else {
        const data: CatImage[] = await get(
          `/images/search?limit=${customLimit}&order=RAND${
            selectedBreed ? `&breed_ids=${selectedBreed}` : ""
          }`
        );
        setCats(Array.isArray(data) ? data : []);
      }
    } finally {
      setLoading(false);
    }
  }, [selectedBreed, limitMode, customLimit]);

  useEffect(() => {
    fetchCats();
  }, []);

  return (
    <div className="app">
      <header>
        <h1>CatAPI</h1>
      </header>

      <main>
        <div className="controls">
          <select
            value={selectedBreed}
            onChange={(e) => setSelectedBreed(e.target.value)}
          >
            <option value="">Alle Rassen</option>
            {breeds.map((b) => (
              <option key={b.id} value={b.id}>
                {b.name}
              </option>
            ))}
          </select>

          <div className="divider" />

          <select
            value={limitMode}
            onChange={(e) => setLimitMode(e.target.value as "all" | "custom")}
          >
            <option value="custom">Anzahl wählen</option>
            <option value="all">Alle anzeigen</option>
          </select>

          {limitMode === "custom" && (
            <input
              type="number"
              min={1}
              max={100}
              value={customLimit}
              onChange={(e) =>
                setCustomLimit(Math.min(100, Math.max(1, Number(e.target.value))))
              }
              placeholder="Anzahl"
            />
          )}

          <div className="divider" />

          <button className="btn" onClick={fetchCats} disabled={loading}>
            <span className={loading ? "spinner" : ""}>↻</span>
            {loading ? "Laden…" : "Laden"}
          </button>
        </div>

        {!loading && cats.length === 0 && (
          <div className="empty-state">
            <p>Keine Bilder gefunden.</p>
          </div>
        )}

        {cats.length > 0 && (
          <div className="grid">
            {cats.map((cat) => (
              <div className="card" key={cat.id}>
                <img src={cat.url} alt="cat" loading="lazy" />
                {cat.breeds && cat.breeds.length > 0 && (
                  <div className="card-info">
                    {cat.breeds.map((b) => (
                      <span className="breed-tag" key={b.id}>
                        {b.name}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}