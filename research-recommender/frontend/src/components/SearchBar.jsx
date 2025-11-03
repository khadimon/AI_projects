import React, { useState, useEffect } from "react";
import "./SearchBar.css";

export default function SearchBar() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [status, setStatus] = useState("");
    const [darkMode, setDarkMode] = useState(true);
    const [sourceFilter, setSourceFilter] = useState("");
    const [yearFilter, setYearFilter] = useState("");
    
    // Update body class for dark/light mode
    useEffect(() => {
        document.body.className = darkMode ? "dark-mode" : "light-mode";
    }, [darkMode]);

    const handleSearch = async () => {
        if (!query) return;
        setStatus("Loading...");
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/search?q=${query}`);
            const data = await response.json();
            setResults(data.papers || []);
            setStatus(data.papers?.length ? "" : "No papers found");
        } 
        catch (error) {
            console.error("Error fetching papers:", error);
            setStatus("Error fetching papers");
        }
    };

    // Filter results
    const filteredResults = results.filter((paper) => {
        let year = null;
        if (paper.published) {
        const match = paper.published.match(/\d{4}$/);
        year = match ? parseInt(match[0]) : null;
        }
    const sourceMatch = sourceFilter ? paper.source === sourceFilter : true;
    const yearMatch = yearFilter ? year === parseInt(yearFilter) : true;
    return sourceMatch && yearMatch;
    });

    return (
        <div className={`search-bar-container ${darkMode ? "dark" : "light"}`}>
            <div className="header-row">
                <h1>Research Paper Recommender</h1>
                <button className="mode-toggle" onClick={() => setDarkMode(!darkMode)}>
                {darkMode ? "Light Mode" : "Dark Mode"}
                </button>
            </div>

            <div className="search-form">
                <input
                type="text"
                placeholder="Search papers..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                />
                <button onClick={handleSearch}>Search</button>
            </div>

            <div className="filters">
                <label>
                Source:
                <select className="search-input" value={sourceFilter} onChange={(e) => setSourceFilter(e.target.value)}>
                    <option value="">All</option>
                    <option value="arXiv">arXiv</option>
                    <option value="IEEE">IEEE</option>
                    <option value="Semantic Scholar">Semantic Scholar</option>
                </select>
                </label>

                <label>
                Year:
                <input
                    className="search-input"
                    type="number"
                    placeholder="e.g. 2021"
                    value={yearFilter}
                    onChange={(e) => setYearFilter(e.target.value)}
                />
                </label>
            </div>

            {status && <p className={`status ${status.includes("Error") ? "error" : ""}`}>{status}</p>}

            <div className="papers-container">
                {filteredResults.map((paper, index) => (
                <div className="paper-card" key={index}>
                    <h2>{paper.title}</h2>
                    <p className="meta">
                    <span>{paper.source}</span> | <span>{paper.published}</span>
                    </p>
                    <p><strong>Authors:</strong> {paper.authors}</p>
                    {paper.summary && <p className="summary">{paper.summary}</p>}
                    <a href={paper.link} target="_blank" rel="noopener noreferrer">
                    Read Paper
                    </a>
                </div>
                ))}
            </div>
        </div>);
}
