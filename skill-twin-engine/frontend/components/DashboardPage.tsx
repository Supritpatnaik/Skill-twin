import React, { useState, ChangeEvent } from 'react';
import ThemeToggle from './ThemeToggle';
import EvolutionTree from './EvolutionTree';
import IntelligenceEngine from './IntelligenceEngine';
import MarketTrends from './MarketTrends';
import ResourceFinder from './ResourceFinder';

const roles = ["SDE / Software Engineer Fresher", "Full Stack Developer", "Python Developer", "Data Analyst", "Machine Learning Engineer", "DevOps Engineer"];
const subjectsList = ["Python", "DSA", "Communication", "SQL"];

const DashboardPage: React.FC<any> = ({ isDarkMode, toggleTheme, onLogoClick }) => {
    const [activeTab, setActiveTab] = useState('readiness'); // 'readiness' or 'resume'
    const [selectedRole, setSelectedRole] = useState(roles[0]);
    const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
    const [questions, setQuestions] = useState<any[]>([]);
    const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
    const [analysis, setAnalysis] = useState<any>(null);
    const [step, setStep] = useState<'setup' | 'quiz' | 'results'>('setup');
    const [loading, setLoading] = useState(false);

    // State for Resume Analyzer
    const [studentName, setStudentName] = useState('');
    const [branch, setBranch] = useState('');
    const [currentYear, setCurrentYear] = useState('');
    const [resumeFile, setResumeFile] = useState<File | null>(null);
    const [syllabusFile, setSyllabusFile] = useState<File | null>(null);
    const [analyzerStep, setAnalyzerStep] = useState<'upload' | 'analysis'>('upload');
    const [extractedSkills, setExtractedSkills] = useState<string[]>([]);
    const [gaps, setGaps] = useState<any[]>([]);
    const [roadmap, setRoadmap] = useState<any>(null);


    const handleFileChange = (e: ChangeEvent<HTMLInputElement>, setFile: React.Dispatch<React.SetStateAction<File | null>>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleStart = async () => {
        if (selectedSubjects.length === 0) return alert("Select subjects!");
        setLoading(true);
        try {
            const res = await fetch('http://localhost:5000/api/questions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subjects: selectedSubjects }),
            });
            const data = await res.json();
            setQuestions(data);
            setStep('quiz');
        } catch (e) { alert("Server error. Run backend!"); }
        finally { setLoading(false); }
    };

    const submitTest = async () => {
        setLoading(true);
        const results = questions.map((q, i) => ({ subject: q.subject, isCorrect: userAnswers[i] === q.answer }));
        try {
            const res = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role: selectedRole, results })
            });
            setAnalysis(await res.json());
            setStep('results');
            window.scrollTo(0,0);
        } catch (e) { alert("Analysis failed!"); }
        finally { setLoading(false); }
    };

    const analyzeDocuments = async () => {
        if (!resumeFile && !syllabusFile) return alert("Please upload at least one document (Resume or Syllabus).");
        setLoading(true);
        try {
            let combinedSkills: string[] = [];
            
            // 1. Parse Resume
            if (resumeFile) {
                const formData = new FormData();
                formData.append('file', resumeFile);
                const resumeRes = await fetch('http://localhost:5000/api/parse-resume', {
                    method: 'POST',
                    body: formData
                });
                const resumeData = await resumeRes.json();
                if (resumeData.validated_skills) {
                    combinedSkills = [...combinedSkills, ...resumeData.validated_skills];
                }
            }

            // 2. Parse Syllabus
            if (syllabusFile) {
                const formData = new FormData();
                formData.append('file', syllabusFile);
                // We reuse the parse-resume endpoint as it just extracts skills from PDF
                const syllabusRes = await fetch('http://localhost:5000/api/parse-resume', {
                    method: 'POST',
                    body: formData
                });
                const syllabusData = await syllabusRes.json();
                if (syllabusData.validated_skills) {
                    combinedSkills = [...combinedSkills, ...syllabusData.validated_skills];
                }
            }

            // Deduplicate skills
            const uniqueSkills = Array.from(new Set(combinedSkills));
            setExtractedSkills(uniqueSkills);

            if (uniqueSkills.length === 0) alert("No valid skills found in uploaded documents. Proceeding anyway.");

            // 3. Get Job Requirements
            const jobRes = await fetch('http://localhost:5000/api/job-requirements', {
               method: 'POST',
               headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify({ role: selectedRole })
            });
            const jobData = await jobRes.json();
            const jobSkills = jobData.required_skills || [];

            // 4. Analyze Gaps
            const gapsRes = await fetch('http://localhost:5000/api/analyze-gaps', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ known_skills: uniqueSkills, job_skills: jobSkills })
            });
            const gapsData = await gapsRes.json();
            const calculatedGaps = gapsData.gaps || [];
            setGaps(calculatedGaps);

            // 5. Generate Roadmap
            if (calculatedGaps.length > 0) {
                 const roadmapRes = await fetch('http://localhost:5000/api/generate-roadmap', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ gaps: calculatedGaps, weeks: 8 })
                });
                const roadmapData = await roadmapRes.json();
                setRoadmap(roadmapData.roadmap);
            } else {
                setRoadmap(null);
            }

            setAnalyzerStep('analysis');

        } catch (e: any) {
            alert("Analysis failed: " + e.message);
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const FileUploadButton: React.FC<{
        label: string;
        file: File | null;
        onFileChange: (e: ChangeEvent<HTMLInputElement>) => void;
        acceptedTypes: string;
    }> = ({ label, file, onFileChange, acceptedTypes }) => (
        <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">{label}</label>
            <label className="w-full bg-white/5 border border-white/10 p-3 rounded-xl flex items-center justify-between cursor-pointer hover:border-primary/50 transition-all">
                <span className={file ? "text-primary font-semibold truncate max-w-[200px]" : "text-gray-500"}>{file ? file.name : "Choose a file..."}</span>
                <span className="material-icons text-gray-400">upload_file</span>
                <input type="file" className="hidden" onChange={onFileChange} accept={acceptedTypes} />
            </label>
        </div>
    );


    return (
        <div className="min-h-screen bg-background-dark text-white font-sans">
            {/* Top Navbar */}
            <header className="fixed top-0 w-full z-50 bg-background-dark/80 backdrop-blur-md border-b border-border-dark px-6 py-4">
                <div className="max-w-[1600px] mx-auto flex justify-between items-center">
                    <div onClick={onLogoClick} className="flex items-center gap-2 cursor-pointer">
                        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                            <span className="material-icons text-white text-xl">architecture</span>
                        </div>
                        <span className="text-xl font-black tracking-tighter uppercase">Skill<span className="text-primary">Twin</span></span>
                    </div>
                    <ThemeToggle isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
                </div>
            </header>

            <div className="flex pt-20">
                {/* Left Sidebar Navigation */}
                <aside className="fixed left-0 w-72 h-[calc(100vh-80px)] border-r border-border-dark bg-surface-dark p-6 overflow-y-auto hidden lg:block">
                    <div className="space-y-2">
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-4 px-2">Main Menu</p>
                        
                        <button 
                            onClick={() => setActiveTab('readiness')}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'readiness' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="material-icons text-sm">bolt</span>
                            <span className="text-sm font-bold">Skill-Readiness</span>
                        </button>

                        <button 
                            onClick={() => setActiveTab('resume')}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'resume' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="material-icons text-sm">description</span>
                            <span className="text-sm font-bold">Skill-Twin Resume Analyzer</span>
                        </button>

                        <button 
                            onClick={() => setActiveTab('intelligence')}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'intelligence' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="material-icons text-sm">public</span>
                            <span className="text-sm font-bold">Live Scraping</span>
                        </button>

                         <button 
                            onClick={() => setActiveTab('evolution')}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'evolution' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="material-icons text-sm">history_edu</span>
                            <span className="text-sm font-bold">Tech Evolution</span>
                        </button>

                        <button 
                            onClick={() => setActiveTab('trends')}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'trends' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="material-icons text-sm">trending_up</span>
                            <span className="text-sm font-bold">Market Trends</span>
                        </button>

                         <button 
                            onClick={() => setActiveTab('learning')}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === 'learning' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-gray-400 hover:bg-white/5'}`}
                        >
                            <span className="material-icons text-sm">school</span>
                            <span className="text-sm font-bold">Resource Finder</span>
                        </button>
                    </div>

                    <div className="mt-10 pt-10 border-t border-border-dark">
                         <div className="p-4 bg-primary/5 rounded-2xl border border-primary/10">
                            <p className="text-xs text-primary font-bold mb-1">Pro Tip</p>
                            <p className="text-[11px] text-gray-500 leading-relaxed">Complete your Skill-Readiness test to get a personalized Resume improvement score.</p>
                         </div>
                    </div>
                </aside>

                {/* Main Content Scroll Area */}
                <main className="flex-1 lg:ml-72 p-8 min-h-screen">
                    <div className="max-w-5xl mx-auto">
                        {activeTab === 'readiness' && (
                            <>
                                {step === 'setup' && (
                                    <div className="max-w-md mx-auto mt-10 bg-surface-dark p-8 rounded-3xl border border-border-dark shadow-2xl">
                                        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">Assessment Setup</h2>
                                        <div className="space-y-4">
                                            <select value={selectedRole} onChange={(e) => setSelectedRole(e.target.value)} className="w-full bg-white/5 border border-white/10 p-3 rounded-xl">
                                                {roles.map(r => <option key={r} value={r} className="bg-black">{r}</option>)}
                                            </select>
                                            <div className="grid grid-cols-2 gap-2">
                                                {subjectsList.map(s => (
                                                    <button key={s} onClick={() => setSelectedSubjects(prev => prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s])}
                                                        className={`p-3 rounded-xl border text-xs ${selectedSubjects.includes(s) ? 'border-primary bg-primary/10' : 'border-white/10'}`}>
                                                        {s}
                                                    </button>
                                                ))}
                                            </div>
                                            <button onClick={handleStart} className="w-full py-4 bg-primary rounded-xl font-bold mt-4 shadow-lg shadow-primary/20">Generate Assessment</button>
                                        </div>
                                    </div>
                                )}

                                {step === 'quiz' && (
                                    <div className="space-y-6">
                                        {questions.map((q, i) => (
                                            <div key={i} className="bg-surface-dark p-6 rounded-2xl border border-border-dark">
                                                <p className="mb-2 text-primary text-[10px] font-bold tracking-widest uppercase">{q.subject}</p>
                                                <p className="text-lg mb-6">Q{i+1}: {q.question}</p>
                                                <div className="grid gap-2">
                                                    {q.options.map(opt => (
                                                        <button key={opt} onClick={() => setUserAnswers({...userAnswers, [i]: opt})}
                                                            className={`text-left p-4 rounded-xl border transition-all ${userAnswers[i] === opt ? 'border-primary bg-primary/10' : 'border-white/5 bg-white/5 hover:border-white/20'}`}>
                                                            {opt}
                                                        </button>
                                                    ))}
                                                </div>
                                            </div>
                                        ))}
                                        <button onClick={submitTest} className="w-full py-5 bg-primary rounded-2xl font-bold text-xl">{loading ? "Analyzing..." : "Submit for Gap Analysis"}</button>
                                    </div>
                                )}

                                {step === 'results' && analysis && (
                                    <div className="space-y-8 pb-20 animate-in fade-in">
                                        {/* Proficiency Graph (CSS Based) */}
                                        <div className="bg-surface-dark p-8 rounded-3xl border border-border-dark">
                                            <h3 className="text-xl font-bold mb-8">Performance Analysis</h3>
                                            <div className="space-y-6">
                                                {analysis.graph_data.map((item: any) => (
                                                    <div key={item.subject}>
                                                        <div className="flex justify-between text-sm mb-2 text-gray-400">
                                                            <span>{item.subject}</span>
                                                            <span className="text-primary font-bold">{item.score}%</span>
                                                        </div>
                                                        <div className="w-full bg-white/5 h-3 rounded-full overflow-hidden">
                                                            <div className="bg-primary h-full transition-all duration-1000" style={{ width: `${item.score}%` }}></div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>

                                        {/* Strengths & Weaknesses */}
                                        <div className="grid md:grid-cols-2 gap-6">
                                            <div className="bg-surface-dark p-6 rounded-2xl border border-green-500/20 shadow-lg shadow-green-500/5">
                                                <h4 className="font-bold text-green-400 mb-4 flex items-center gap-2">
                                                    <span className="material-icons">task_alt</span> Strengths
                                                </h4>
                                                <ul className="text-sm text-gray-400 space-y-2">
                                                    {analysis.ai_analysis.strengths.map((s:string) => <li key={s}>• {s}</li>)}
                                                </ul>
                                            </div>
                                            <div className="bg-surface-dark p-6 rounded-2xl border border-red-500/20 shadow-lg shadow-red-500/5">
                                                <h4 className="font-bold text-red-400 mb-4 flex items-center gap-2">
                                                    <span className="material-icons">emergency</span> Critical Gaps
                                                </h4>
                                                <ul className="text-sm text-gray-400 space-y-2">
                                                    {analysis.ai_analysis.weaknesses.map((w:string) => <li key={w}>• {w}</li>)}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </>
                        )}
                        
                        {activeTab === 'resume' && (
                            // RESUME ANALYZER TAB
                            <>
                                {analyzerStep === 'upload' ? (
                                    <div className="max-w-2xl mx-auto mt-10 animate-in fade-in">
                                        <div className="text-center mb-10">
                                            <h2 className="text-3xl font-bold mb-2">Skill-Twin Resume Analyzer</h2>
                                            <p className="text-gray-500">Upload your documents to get a personalized analysis based on your academic background.</p>
                                        </div>
                                        <div className="bg-surface-dark p-8 rounded-3xl border border-border-dark shadow-2xl space-y-6">
                                            <div>
                                                <label htmlFor="name" className="block text-sm font-medium text-gray-400 mb-2">Your Name</label>
                                                <input type="text" id="name" value={studentName} onChange={(e) => setStudentName(e.target.value)} className="w-full bg-white/5 border border-white/10 p-3 rounded-xl" placeholder="e.g. Suprit Kumar Patnaik"/>
                                            </div>
                                            
                                            <div>
                                                <label htmlFor="targetRole" className="block text-sm font-medium text-gray-400 mb-2">Target Role</label>
                                                <select id="targetRole" value={selectedRole} onChange={(e) => setSelectedRole(e.target.value)} className="w-full bg-white/5 border border-white/10 p-3 rounded-xl">
                                                    {roles.map(r => <option key={r} value={r} className="bg-black">{r}</option>)}
                                                </select>
                                            </div>
                                            
                                            <div className="grid grid-cols-2 gap-6">
                                                <div>
                                                    <label htmlFor="branch" className="block text-sm font-medium text-gray-400 mb-2">Your Branch</label>
                                                    <input type="text" id="branch" value={branch} onChange={(e) => setBranch(e.target.value)} className="w-full bg-white/5 border border-white/10 p-3 rounded-xl" placeholder="e.g. Computer Science"/>
                                                </div>
                                                <div>
                                                    <label htmlFor="year" className="block text-sm font-medium text-gray-400 mb-2">Current Year</label>
                                                    <select id="year" value={currentYear} onChange={(e) => setCurrentYear(e.target.value)} className="w-full bg-white/5 border border-white/10 p-3 rounded-xl">
                                                        <option value="" className="bg-black">Select Year...</option>
                                                        <option value="1" className="bg-black">1st Year</option>
                                                        <option value="2" className="bg-black">2nd Year</option>
                                                        <option value="3" className="bg-black">3rd Year</option>
                                                        <option value="4" className="bg-black">4th Year</option>
                                                        <option value="graduate" className="bg-black">Graduate</option>
                                                    </select>
                                                </div>
                                            </div>
                                            <FileUploadButton label="Upload Resume" file={resumeFile} onFileChange={(e) => handleFileChange(e, setResumeFile)} acceptedTypes=".pdf" />
                                            <FileUploadButton label="Upload Syllabus" file={syllabusFile} onFileChange={(e) => handleFileChange(e, setSyllabusFile)} acceptedTypes=".pdf" />
                                            
                                            <button 
                                                onClick={analyzeDocuments}
                                                className="w-full py-4 bg-primary rounded-xl font-bold mt-4 shadow-lg shadow-primary/20 disabled:bg-gray-600 disabled:shadow-none flex items-center justify-center gap-2"
                                                disabled={!studentName || !branch || !currentYear || (!resumeFile && !syllabusFile) || loading}
                                            >
                                                {loading ? (
                                                    <>
                                                        <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
                                                        Analyzing...
                                                    </>
                                                ) : (
                                                    "Analyze Documents"
                                                )}
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-8 pb-20 animate-in fade-in">
                                         <button onClick={() => setAnalyzerStep('upload')} className="text-gray-400 hover:text-white flex items-center gap-2 mb-4">
                                            <span className="material-icons text-sm">arrow_back</span> Back to Upload
                                        </button>

                                        {/* 1. Analyzed Skills */}
                                        <div className="bg-surface-dark p-8 rounded-3xl border border-border-dark">
                                            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                                                <span className="material-icons text-primary">analytics</span> 
                                                Extracted Skills
                                            </h3>
                                            <div className="flex flex-wrap gap-2">
                                                {extractedSkills.map(skill => (
                                                    <span key={skill} className="px-3 py-1 bg-white/5 rounded-full text-sm border border-white/10 text-gray-300">
                                                        {skill}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>

                                        {/* 2. Gaps */}
                                        <div className="bg-surface-dark p-8 rounded-3xl border border-border-dark">
                                            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                                                <span className="material-icons text-red-400">difference</span> 
                                                Skill Gaps for {selectedRole}
                                            </h3>
                                            {gaps.length > 0 ? (
                                                <div className="overflow-x-auto">
                                                    <table className="w-full text-left text-sm text-gray-400">
                                                        <thead className="text-xs uppercase bg-white/5 text-gray-300">
                                                            <tr>
                                                                <th className="px-4 py-3 rounded-tl-lg">Missing Skill</th>
                                                                <th className="px-4 py-3">Gap Level</th>
                                                                <th className="px-4 py-3 rounded-tr-lg">Match Score</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {gaps.map((gap: any) => (
                                                                <tr key={gap.skill} className="border-b border-white/5 hover:bg-white/5">
                                                                    <td className="px-4 py-3 font-medium text-white">{gap.skill}</td>
                                                                    <td className="px-4 py-3">
                                                                        <span className={`px-2 py-1 rounded text-xs font-bold ${gap.level === 'High' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                                                                            {gap.level}
                                                                        </span>
                                                                    </td>
                                                                    <td className="px-4 py-3 text-gray-500">{gap.match}</td>
                                                                </tr>
                                                            ))}
                                                        </tbody>
                                                    </table>
                                                </div>
                                            ) : (
                                                <p className="text-green-400">Great! No major skill gaps found for this role.</p>
                                            )}
                                        </div>

                                         {/* 3. Roadmap */}
                                         {roadmap && (
                                            <div className="space-y-4">
                                                <h3 className="text-2xl font-bold mb-6">Personalized Learning Roadmap</h3>
                                                {roadmap.roadmap?.map((week: any, idx: number) => (
                                                    <div key={idx} className="bg-surface-dark p-6 rounded-2xl border border-border-dark">
                                                        <div className="flex justify-between items-start mb-4">
                                                             <h4 className="text-lg font-bold text-primary">Week {week.week}</h4>
                                                             <span className="text-xs text-gray-500 bg-white/5 px-2 py-1 rounded">{week.hours} Hours</span>
                                                        </div>
                                                        <div className="space-y-4">
                                                            {week.focus_skills.map((skillItem: any, i:number) => {
                                                                let skillName = "";
                                                                let recommendations = "";

                                                                if (typeof skillItem === 'string') {
                                                                    skillName = skillItem;
                                                                } else if (Array.isArray(skillItem) && skillItem.length >= 2) {
                                                                    skillName = skillItem[0];
                                                                    recommendations = skillItem[1];
                                                                } else if (typeof skillItem === 'object' && skillItem !== null) {
                                                                     // Handle object case { skill: "...", recommendations: "..." } or similar keys
                                                                     skillName = skillItem.skill || skillItem.name || "Unknown Skill";
                                                                     recommendations = skillItem.recommendations || skillItem.description || "";
                                                                }

                                                                return (
                                                                    <div key={i} className="pl-4 border-l-2 border-primary/20">
                                                                        <p className="font-bold text-white mb-1">{skillName}</p>
                                                                        {recommendations && (
                                                                            <p className="text-sm text-gray-400 leading-relaxed">{recommendations}</p>
                                                                        )}
                                                                    </div>
                                                                );
                                                            })}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                         )}
                                    </div>
                                )}
                            </>
                        )}

                        {activeTab === 'evolution' && (
                            <div className="animate-in fade-in">
                                <EvolutionTree onBack={() => setActiveTab('readiness')} />
                            </div>
                        )}

                        {activeTab === 'trends' && (
                            <div className="animate-in fade-in h-[calc(100vh-100px)]">
                                <MarketTrends onBack={() => setActiveTab('readiness')} />
                            </div>
                        )}

                        {activeTab === 'learning' && (
                            <div className="animate-in fade-in h-[calc(100vh-100px)]">
                                <ResourceFinder onBack={() => setActiveTab('readiness')} />
                            </div>
                        )}

                        {activeTab === 'intelligence' && (
                            <div className="animate-in fade-in">
                                <IntelligenceEngine onBack={() => setActiveTab('readiness')} />
                            </div>
                        )}
                    </div>

                </main>
            </div>
        </div>
    );
};

export default DashboardPage;
