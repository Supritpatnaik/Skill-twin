import React, { useState } from "react";

// Mock Data for Trends (replace with API data later)
const TRENDS_DATA: any = {
    "Full Stack Developer": {
        demand: "Very High",
        salary: "$80k - $140k",
        growth: "+22%",
        requiredSkills: ["React", "Node.js", "TypeScript", "PostgreSQL", "AWS", "Docker"],
        emergingSkills: ["Next.js", "GraphQL", "Tailwind CSS"]
    },
    "AI/ML Engineer": {
        demand: "Explosive",
        salary: "$120k - $200k",
        growth: "+45%",
        requiredSkills: ["Python", "PyTorch", "TensorFlow", "NLP", "Computer Vision", "MLOps"],
        emergingSkills: ["LLMs", "RAG", "LangChain", "HuggingFace"]
    },
    "Data Scientist": {
        demand: "High",
        salary: "$95k - $160k",
        growth: "+18%",
        requiredSkills: ["Python", "SQL", "Machine Learning", "TensorFlow", "Pandas", "Statistics"],
        emergingSkills: ["Vector Databases", "Big Data", "Generative AI"]
    },
    "DevOps Engineer": {
        demand: "High",
        salary: "$100k - $150k",
        growth: "+24%",
        requiredSkills: ["Linux", "AWS/Azure", "Kubernetes", "CI/CD", "Terraform", "Python"],
        emergingSkills: ["GitOps", "Prometheus", "Service Mesh"]
    },
    "Product Manager": {
        demand: "Steady",
        salary: "$90k - $160k",
        growth: "+12%",
        requiredSkills: ["Agile", "User Research", "Roadmapping", "Jira", "Data Analytics", "Stakeholder Management"],
        emergingSkills: ["AI Strategy", "Growth Hacking", "No-Code Tools"]
    },
    "Cybersecurity Analyst": {
        demand: "Very High",
        salary: "$85k - $145k",
        growth: "+30%",
        requiredSkills: ["Network Security", "Ethical Hacking", "SIEM", "Python", "Linux", "Risk Assessment"],
        emergingSkills: ["Cloud Security", "Zero Trust", "AI Security Defense"]
    },
    "Mobile App Developer": {
        demand: "Moderate",
        salary: "$80k - $135k",
        growth: "+15%",
        requiredSkills: ["React Native", "Flutter", "Swift", "Kotlin", "Firebase", "REST APIs"],
        emergingSkills: ["SwiftUI", "Jetpack Compose", "Mobile AI"]
    },
    "UI/UX Designer": {
        demand: "High",
        salary: "$75k - $130k",
        growth: "+14%",
        requiredSkills: ["Figma", "Wireframing", "Prototyping", "User Testing", "Adobe XD", "HTML/CSS Basics"],
        emergingSkills: ["Design Systems", "3D Design (Spline)", "AI Design Tools"]
    },
    "Cloud Architect": {
        demand: "High",
        salary: "$130k - $190k",
        growth: "+20%",
        requiredSkills: ["AWS/Azure/GCP", "System Design", "Networking", "Security Compliance", "Microservices", "Cost Optimization"],
        emergingSkills: ["Serverless", "Multi-Cloud Strategy", "Edge Computing"]
    },
    "Blockchain Developer": {
        demand: "Niche",
        salary: "$100k - $170k",
        growth: "+10%",
        requiredSkills: ["Solidity", "Rust", "Smart Contracts", "Web3.js", "Cryptography", "Ethereum"],
        emergingSkills: ["DeFi", "NFTs", "ZK-Rollups"]
    }
};

const MarketTrends: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [selectedRole, setSelectedRole] = useState("Full Stack Developer");
    const [userSkills, setUserSkills] = useState<string[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [roadmap, setRoadmap] = useState<any>(null);

    // Simulated Resume Upload handling (simplified for this view) or Manual Input
    const [manualSkillInput, setManualSkillInput] = useState("");

    const handleAddSkills = () => {
        if (!manualSkillInput) return;
        const newSkills = manualSkillInput.split(',').map(s => s.trim()).filter(Boolean);
        setUserSkills(prev => [...Array.from(new Set([...prev, ...newSkills]))]);
        setManualSkillInput("");
    };

    const generateRoadmap = async () => {
        setIsAnalyzing(true);
        // Simulating AI delay
        setTimeout(() => {
            const roleData = TRENDS_DATA[selectedRole as keyof typeof TRENDS_DATA];
            const missing = roleData.requiredSkills.filter((s: string) => !userSkills.map(us => us.toLowerCase()).includes(s.toLowerCase()));
            const matchCount = roleData.requiredSkills.length - missing.length;
            const score = Math.round((matchCount / roleData.requiredSkills.length) * 100);

            setRoadmap({
                score,
                missingSkills: missing,
                projectedScore: Math.min(score + 30, 95),
                steps: missing.map((skill: string, i: number) => ({
                    week: `Week ${i + 1}`,
                    action: `Master ${skill}`,
                    resource: `Build a project using ${skill}`
                }))
            });
            setIsAnalyzing(false);
        }, 2000);
    };

    return (
        <div className="h-full p-6 md:p-12 text-white bg-surface-dark overflow-y-auto rounded-3xl border border-border-dark selection:bg-primary/30">
            <div className="max-w-6xl mx-auto space-y-12">

                {/* Header */}
                <header className="flex justify-between items-center">
                    <div>
                        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-green-400 mb-2">Market Intelligence</h1>
                        <p className="text-gray-400">Live job market trends tailored to your profile.</p>
                    </div>
                    <button onClick={onBack} className="text-sm text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-white/5">
                        ← Back to Menu
                    </button>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                    {/* LEFT: Market Trends Selector */}
                    <div className="lg:col-span-2 space-y-8">
                        <div className="bg-surface-dark p-6 rounded-2xl border border-white/10 shadow-xl">
                            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                                <span>📈</span> Current Industry Pulse
                            </h2>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                                {Object.keys(TRENDS_DATA).map((role) => (
                                    <button
                                        key={role}
                                        onClick={() => { setSelectedRole(role); setRoadmap(null); }}
                                        className={`p-4 rounded-xl border text-left transition-all ${selectedRole === role
                                            ? "bg-primary/20 border-primary shadow-lg shadow-primary/10"
                                            : "bg-white/5 border-white/10 hover:bg-white/10"
                                            }`}
                                    >
                                        <div className="font-bold mb-1">{role}</div>
                                        <div className="text-xs text-gray-400">
                                            Demand: <span className="text-emerald-400">{TRENDS_DATA[role as keyof typeof TRENDS_DATA].demand}</span>
                                        </div>
                                    </button>
                                ))}
                            </div>

                            {/* Selected Role Snapshot */}
                            <div className="p-6 bg-white/5 rounded-2xl border border-white/10">
                                <div className="flex justify-between items-start mb-6">
                                    <div>
                                        <h3 className="text-2xl font-bold">{selectedRole}</h3>
                                        <div className="flex gap-4 text-sm text-gray-400 mt-1">
                                            <span>Salary: {TRENDS_DATA[selectedRole as keyof typeof TRENDS_DATA].salary}</span>
                                            <span>•</span>
                                            <span className="text-emerald-400">Growth: {TRENDS_DATA[selectedRole as keyof typeof TRENDS_DATA].growth}</span>
                                        </div>
                                    </div>
                                    <div className="px-3 py-1 bg-white/10 rounded-full text-xs font-mono">Live Data</div>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Required Tech Stack</p>
                                        <div className="flex flex-wrap gap-2">
                                            {TRENDS_DATA[selectedRole as keyof typeof TRENDS_DATA].requiredSkills.map((skill: string) => (
                                                <span key={skill} className="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-300 text-sm">
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                    <div>
                                        <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 mt-4">Emerging / Bonus Skills</p>
                                        <div className="flex flex-wrap gap-2">
                                            {TRENDS_DATA[selectedRole as keyof typeof TRENDS_DATA].emergingSkills.map((skill: string) => (
                                                <span key={skill} className="px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-sm">
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* AI Mentorship / Roadmap Result */}
                        {roadmap && (
                            <div className="bg-surface-dark p-6 rounded-2xl border-t-4 border-t-primary animate-in slide-in-from-bottom-5 fade-in duration-700 shadow-2xl">
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-2xl font-bold">🚀 Personalized Career Roadmap</h2>
                                    <div className="text-right">
                                        <p className="text-xs text-gray-400">Projected Employability</p>
                                        <p className="text-xl font-bold text-emerald-400">{roadmap.score}% <span className="text-gray-500">→</span> {roadmap.projectedScore}%</p>
                                    </div>
                                </div>

                                <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
                                    <p className="text-sm font-bold text-red-300 mb-2">⚠️ Missing Critical Skills</p>
                                    <p className="text-sm text-gray-300">
                                        You need to add <span className="font-bold text-white">{roadmap.missingSkills.join(", ")}</span> to your arsenal to qualify for 80% of open roles.
                                    </p>
                                </div>

                                <div className="space-y-4 relative before:absolute before:inset-0 before:ml-6 before:w-0.5 before:bg-white/10">
                                    {roadmap.steps.map((step: any, index: number) => (
                                        <div key={index} className="relative pl-12">
                                            <div className="absolute left-4 top-2 w-4 h-4 rounded-full bg-primary border-4 border-[#0f1115]"></div>
                                            <div className="p-4 bg-white/5 rounded-xl border border-white/10 hover:bg-white/10 transition-colors">
                                                <p className="text-xs font-bold text-primary mb-1">{step.week}</p>
                                                <h4 className="font-bold mb-1">{step.action}</h4>
                                                <p className="text-sm text-gray-400">{step.resource}</p>
                                            </div>
                                        </div>
                                    ))}
                                    <div className="relative pl-12">
                                        <div className="absolute left-4 top-2 w-4 h-4 rounded-full bg-emerald-500 border-4 border-[#0f1115]"></div>
                                        <div className="p-4 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
                                            <h4 className="font-bold text-emerald-400">🎉 Job Ready!</h4>
                                            <p className="text-sm text-emerald-200/70">Apply for Junior/Mid-level {selectedRole} roles.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* RIGHT: User Profile Context */}
                    <div className="space-y-6">
                        <div className="bg-surface-dark p-6 rounded-2xl border border-white/10 sticky top-6 shadow-xl">
                            <h2 className="text-xl font-bold mb-4">👤 Your Context</h2>
                            <p className="text-sm text-gray-400 mb-6">
                                Add your skills or upload a resume to unlock personalized gap analysis against these trends.
                            </p>

                            <div className="space-y-4">
                                {/* Simplified Skills Input */}
                                <div>
                                    <label className="text-xs font-bold text-gray-500 uppercase">My Skills</label>
                                    <div className="flex gap-2 mt-2">
                                        <input
                                            type="text"
                                            value={manualSkillInput}
                                            onChange={(e) => setManualSkillInput(e.target.value)}
                                            placeholder="e.g. React, Python..."
                                            className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary text-white"
                                            onKeyDown={(e) => e.key === 'Enter' && handleAddSkills()}
                                        />
                                        <button
                                            onClick={handleAddSkills}
                                            className="px-3 py-2 bg-primary/20 hover:bg-primary/30 text-primary rounded-lg text-sm font-bold"
                                        >
                                            +
                                        </button>
                                    </div>
                                    <div className="flex flex-wrap gap-2 mt-3">
                                        {userSkills.map((skill, i) => (
                                            <span key={i} className="px-2 py-1 bg-white/10 rounded text-xs flex items-center gap-1">
                                                {skill}
                                                <button onClick={() => setUserSkills(prev => prev.filter(s => s !== skill))} className="hover:text-red-400">×</button>
                                            </span>
                                        ))}
                                        {userSkills.length === 0 && (
                                            <span className="text-xs text-gray-600 italic">No skills added yet.</span>
                                        )}
                                    </div>
                                </div>

                                <div className="h-px bg-white/10 my-4"></div>

                                <button
                                    onClick={generateRoadmap}
                                    disabled={userSkills.length === 0 || isAnalyzing}
                                    className="w-full py-4 rounded-xl bg-gradient-to-r from-primary to-purple-600 font-bold hover:shadow-lg hover:shadow-primary/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
                                >
                                    {isAnalyzing ? (
                                        <>
                                            <div className="h-4 w-4 border-2 border-white/50 border-t-white rounded-full animate-spin"></div>
                                            Analyzing Gaps...
                                        </>
                                    ) : (
                                        <>
                                            ⚡ Generate Mentorship Plan
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default MarketTrends;
