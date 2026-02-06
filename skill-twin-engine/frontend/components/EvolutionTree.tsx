import React, { useState } from "react";

const TIMELINE_DATA = [
    {
        era: "1995–2005",
        title: "Web Foundation",
        color: "from-blue-500 to-cyan-400",
        skills: ["HTML", "CSS", "JavaScript", "PHP", "Java"],
        description: "The dawn of the internet. Static pages evolved into dynamic web applications."
    },
    {
        era: "2006–2012",
        title: "Cloud & Mobile",
        color: "from-cyan-400 to-emerald-400",
        skills: ["AWS", "Azure", "Virtualization", "iOS/Android", "REST APIs"],
        description: "Infrastructure shifted to the cloud, and the world went mobile-first."
    },
    {
        era: "2010–2018",
        title: "Big Data Era",
        color: "from-emerald-400 to-indigo-500",
        skills: ["Python", "SQL", "Hadoop", "Spark", "Data Pipelines"],
        description: "Data became the new oil. Processing massive datasets became reliable."
    },
    {
        era: "2014–2022",
        title: "ML & Deep Learning",
        color: "from-indigo-500 to-purple-500",
        skills: ["TensorFlow", "PyTorch", "Neural Nets", "Computer Vision", "NLP"],
        description: "AI moved from theory to practice with deep learning breakthroughs."
    },
    {
        era: "2021–2026",
        title: "Generative AI",
        color: "from-purple-500 to-fuchsia-500",
        skills: ["LLMs", "RAG", "Prompt Eng", "AI Agents", "Multimodal Models"],
        description: "AI starts creating. Large Language Models transform human-computer interaction."
    },
    {
        era: "2026–2028",
        title: "AI Infrastructure",
        color: "from-fuchsia-500 to-pink-500",
        skills: ["MLOps", "AutoML", "Edge AI", "Model Distillation", "Governance"],
        description: "Scaling AI becomes the primary challenge. Ops and compliance maturing."
    },
    {
        era: "2028–2032",
        title: "Symbiotic Era",
        color: "from-pink-500 to-rose-500",
        skills: ["AR/VR Spatial", "BCI Basics", "Human-AI Collab", "Agent Swarms"],
        description: "Blurring lines between physical/digital and human/AI cognition."
    },
    {
        era: "2030+",
        title: "Quantum Leap",
        color: "from-rose-500 to-orange-500",
        skills: ["Qubits", "Quantum Algo", "Cryptography", "Super-Simulation"],
        description: "Computation transcends binary limits. Solving impossible problems."
    }
];

const EvolutionTree: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [activeEra, setActiveEra] = useState<number | null>(null);

    return (
        <div className="h-[80vh] bg-surface-dark text-white overflow-hidden relative selection:bg-purple-500/30 rounded-3xl border border-border-dark flex flex-col">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[100px]"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-[100px]"></div>
            </div>

            <div className="relative z-10 p-8 h-full flex flex-col">
                {/* Header */}
                <header className="flex justify-between items-center mb-12">
                    <div>
                        <h1 className="text-4xl font-extrabold tracking-tight mb-2">
                            Technology <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">Evolution Tree</span>
                        </h1>
                        <p className="text-gray-400">The roadmap of human ingenuity. Where do you stand?</p>
                    </div>
                    <button onClick={onBack} className="px-6 py-2 rounded-full border border-white/10 hover:bg-white/5 transition-all text-sm">
                        ← Back to Menu
                    </button>
                </header>

                {/* Horizontal Tree Visualization */}
                <div className="flex-1 flex items-center overflow-x-auto pb-6 scrollbar-hide w-full">

                    {/* The Trunk (Start) */}
                    <div className="flex items-center">
                        <div className="w-24 h-2 bg-gray-800 rounded-l-full relative">
                            <div className="absolute -left-4 -bottom-8 text-xs font-mono text-gray-600 transform -rotate-90 origin-top-right">ROOTS</div>
                        </div>
                    </div>

                    {/* Branches */}
                    <div className="flex relative">
                        {/* Connecting Line running through */}
                        <div className="absolute top-1/2 left-0 w-full h-1 bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800 -z-10 transform -translate-y-1/2 rounded-full opacity-30"></div>

                        {TIMELINE_DATA.map((item, index) => (
                            <div key={index}
                                className="relative group mx-4 min-w-[200px] flex flex-col items-center justify-center transition-all duration-500"
                                onMouseEnter={() => setActiveEra(index)}
                                onMouseLeave={() => setActiveEra(null)}
                            >
                                {/* Branch Node */}
                                <div className={`
                            w-6 h-6 rounded-full border-4 border-[#050505] shadow-[0_0_20px_rgba(0,0,0,0.5)] z-20 
                            bg-gradient-to-br ${item.color} 
                            ${activeEra === index ? 'scale-150 ring-4 ring-white/10' : 'scale-100'}
                            transition-all duration-300 cursor-pointer
                        `}></div>

                                {/* Era Label (Top) */}
                                <div className={`
                            absolute bottom-12 transition-all duration-300 flex flex-col items-center text-center w-48
                            ${index % 2 === 0 ? 'bottom-12' : 'top-12'}
                            ${activeEra === index ? 'opacity-100 translate-y-0' : 'opacity-60'}
                        `}>
                                    <div className="text-sm font-bold text-gray-500 font-mono mb-1">{item.era}</div>
                                    <div className={`text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r ${item.color}`}>
                                        {item.title}
                                    </div>
                                </div>

                                {/* Leaves/Skills (Popout Info) */}
                                <div className={`
                            absolute left-1/2 -translate-x-1/2 w-64 p-5 rounded-2xl glass-card border border-white/10 bg-[#0a0a0a]/90 backdrop-blur-xl z-50
                            transition-all duration-500 pointer-events-none
                            ${index % 2 === 0 ? 'top-16 origin-top' : 'bottom-16 origin-bottom'}
                            ${activeEra === index ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 translate-y-4'}
                        `}>
                                    <div className={`h-1 w-full bg-gradient-to-r ${item.color} mb-3 rounded-full opacity-50`}></div>
                                    <p className="text-xs text-gray-400 mb-4 leading-relaxed">{item.description}</p>

                                    <div className="flex flex-wrap gap-2">
                                        {item.skills.map(skill => (
                                            <span key={skill} className="px-2 py-1 rounded-md bg-white/5 border border-white/10 text-[10px] font-mono text-gray-300">
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                {/* Connection Line Segment */}
                                {index < TIMELINE_DATA.length - 1 && (
                                    <div className={`
                                absolute top-1/2 left-1/2 w-full h-[2px] -z-10
                                bg-gradient-to-r ${item.color} 
                                opacity-50
                            `}></div>
                                )}
                            </div>
                        ))}

                        {/* Arrow at the end */}
                        <div className="relative flex items-center">
                            <div className="w-12 h-0.5 bg-gradient-to-r from-orange-500 to-transparent"></div>
                            <div className="text-orange-500 text-2xl -ml-2 animate-pulse">›</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EvolutionTree;
