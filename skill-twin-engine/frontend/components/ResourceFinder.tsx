import React, { useState } from "react";

type Resource = {
    platform: "YouTube" | "Coursera" | "Udemy" | "Documentation" | "FreeCodeCamp" | "Other";
    title: string;
    url: string;
    isFree: boolean;
};

type SkillResources = {
    skill: string;
    resources: Resource[];
};

const ResourceFinder: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [results, setResults] = useState<SkillResources[] | null>(null);

    const handleSearch = async () => {
        if (!input.trim()) return;
        setIsLoading(true);
        setResults(null);

        try {
            const response = await fetch("http://localhost:5000/api/find-resources", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: input }),
            });
            const data = await response.json();
            if (data.success) {
                setResults(data.resources);
            }
        } catch (error) {
            console.error("Failed to fetch resources", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="h-full bg-surface-dark text-white p-6 md:p-12 relative overflow-y-auto rounded-3xl border border-border-dark flex flex-col">
            {/* Background Decor */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-green-500/10 rounded-full blur-[120px] pointer-events-none"></div>

            <div className="max-w-4xl mx-auto relative z-10 w-full">
                <header className="mb-12 text-center relative">
                    <button onClick={onBack} className="absolute left-0 top-0 hidden md:block px-4 py-1.5 rounded-full border border-white/10 hover:bg-white/5 text-xs text-gray-400 transition-colors">
                        ← Back to Menu
                    </button>
                     <div className="md:hidden mb-4 text-left">
                        <button onClick={onBack} className="px-4 py-1.5 rounded-full border border-white/10 hover:bg-white/5 text-xs text-gray-400 transition-colors">
                            ← Back
                        </button>
                    </div>
                   
                    <h1 className="text-5xl font-extrabold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-cyan-400">
                        Smart Resource Finder
                    </h1>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        Paste any skill, topic, or course name. We'll curate the best learning paths from across the web.
                    </p>
                </header>

                {/* Input Section */}
                <div className="bg-white/5 p-2 rounded-2xl flex items-center gap-2 border border-white/10 shadow-2xl mb-16">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                        placeholder="e.g. Next.js 14, Advanced Python, Machine Learning..."
                        className="flex-1 bg-transparent border-none outline-none px-6 py-4 text-lg placeholder-gray-500 text-white"
                    />
                    <button
                        onClick={handleSearch}
                        disabled={isLoading || !input}
                        className="px-8 py-4 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600 font-bold text-black hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? "Searching..." : "Find Resources"}
                    </button>
                </div>

                {/* Results Grid */}
                <div className="space-y-12 pb-20">
                    {results && results.map((item, idx) => (
                        <div key={idx} className="animate-in slide-in-from-bottom-5 fade-in duration-500" style={{ animationDelay: `${idx * 100}ms` }}>
                            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                                <span className="w-2 h-8 rounded bg-green-500 block"></span>
                                {item.skill}
                            </h2>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {item.resources.map((res, rIdx) => (
                                    <a
                                        key={rIdx}
                                        href={res.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="group p-5 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-green-500/50 transition-all flex justify-between items-start"
                                    >
                                        <div>
                                            <div className="flex items-center gap-2 mb-2">
                                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${res.platform === 'YouTube' ? 'bg-red-500/20 text-red-500' :
                                                        res.platform === 'Udemy' ? 'bg-purple-500/20 text-purple-400' :
                                                            res.platform === 'Coursera' ? 'bg-blue-500/20 text-blue-400' :
                                                                'bg-gray-700 text-gray-300'
                                                    }`}>
                                                    {res.platform}
                                                </span>
                                                {res.isFree && <span className="text-[10px] bg-green-500/20 text-green-400 px-2 py-0.5 rounded font-bold">FREE</span>}
                                            </div>
                                            <h3 className="font-bold text-lg group-hover:text-green-400 transition-colors leading-snug">{res.title}</h3>
                                        </div>
                                        <div className="text-gray-500 group-hover:text-white transition-colors transform group-hover:translate-x-1">
                                            ↗
                                        </div>
                                    </a>
                                ))}
                            </div>
                        </div>
                    ))}

                    {results && results.length === 0 && !isLoading && (
                        <div className="text-center text-gray-500 py-12">
                            <p>No specific resources found. Try broadening your terms.</p>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
};

export default ResourceFinder;
