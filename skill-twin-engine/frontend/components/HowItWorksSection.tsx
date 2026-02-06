
import React from 'react';
import ScrollAnimatedSection from './ScrollAnimatedSection';

const HowItWorksSection: React.FC = () => {
    return (
        <>
            <ScrollAnimatedSection className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-24 mb-10">
                <div className="text-center mb-16">
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white">How It Works</h2>
                    <p className="text-gray-600 dark:text-gray-400 mt-2">Four steps to your dream job.</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {howItWorksData.map((item, index) => (
                        <div key={index} className="group bg-white dark:bg-card-dark p-6 rounded-2xl border border-gray-200 dark:border-border-dark hover:border-primary/50 dark:hover:border-primary/50 hover:shadow-lg transform hover:-translate-y-1 transition-all duration-300">
                            <div className="w-10 h-10 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center text-gray-900 dark:text-white font-bold mb-4 group-hover:bg-primary group-hover:text-white transition-colors">{index + 1}</div>
                            <div className={`h-12 w-12 rounded-lg flex items-center justify-center mb-4 ${item.colorClass}`}>
                                <span className="material-icons">{item.icon}</span>
                            </div>
                            <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-2">{item.title}</h3>
                            <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{item.description}</p>
                        </div>
                    ))}
                </div>
            </ScrollAnimatedSection>
            <ScrollAnimatedSection className="mt-20 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 group/dashboard">
                <div className="relative rounded-2xl overflow-hidden shadow-2xl shadow-black/50 border border-gray-200 dark:border-border-dark bg-surface-light/80 dark:bg-card-dark/80 backdrop-blur-md transform transition-transform hover:scale-[1.005] duration-500">
                    <div className="flex items-center gap-2 px-4 py-4 bg-gray-50/90 dark:bg-[#0a0a0a]/90 backdrop-blur border-b border-gray-200 dark:border-border-dark">
                        <div className="flex gap-2">
                            <div className="w-3 h-3 rounded-full bg-red-500/80 hover:bg-red-500 transition-colors"></div>
                            <div className="w-3 h-3 rounded-full bg-yellow-500/80 hover:bg-yellow-500 transition-colors"></div>
                            <div className="w-3 h-3 rounded-full bg-green-500/80 hover:bg-green-500 transition-colors"></div>
                        </div>
                        <div className="flex-1 max-w-lg mx-auto bg-white dark:bg-[#1a1a1a] rounded-lg py-1.5 px-4 text-xs text-gray-500 flex items-center justify-between border border-gray-200 dark:border-gray-800 shadow-inner">
                            <span className="opacity-60 font-mono">skill-twin.app/dashboard</span>
                            <span className="material-icons text-[12px] opacity-60">lock</span>
                        </div>
                    </div>
                    <div className="p-6 md:p-10 bg-white/50 dark:bg-background-dark/50 mesh-bg">
                        {/* Dashboard content here */}
                        <DashboardContent />
                    </div>
                </div>
            </ScrollAnimatedSection>
        </>
    );
};

const DashboardContent: React.FC = () => (
    <>
        <div className="bg-surface-light/80 dark:bg-card-dark/80 backdrop-blur-md border border-gray-200 dark:border-border-dark rounded-xl p-6 mb-8">
            {/* User Profile */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">
                <div className="flex items-center gap-5">
                    <div className="relative">
                        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-800 dark:to-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300 font-bold text-xl shadow-lg">SP</div>
                        <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-primary rounded-full border-4 border-surface-light dark:border-card-dark flex items-center justify-center">
                            <span className="material-icons text-white text-[10px]">check</span>
                        </div>
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">Suprit Kumar Patnaik</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">CS Undergrad • Final Year</p>
                    </div>
                </div>
                <div className="w-full sm:w-auto bg-white dark:bg-black/40 rounded-xl p-4 sm:px-8 border border-gray-100 dark:border-gray-800 shadow-sm">
                    <div className="flex items-center justify-between sm:block gap-4">
                        <div className="flex items-center gap-2 mb-1">
                            <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide font-semibold">Job Match Score</p>
                            <span className="relative flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                            </span>
                        </div>
                        <div className="flex items-end gap-2">
                            <p className="text-3xl font-bold text-primary tabular-nums">71%</p>
                            <span className="text-xs text-green-500 font-semibold mb-1 flex items-center"><span className="material-icons text-xs mr-0.5">arrow_upward</span> +29%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Target Role & Progress Bar */}
            <div className="mt-6 flex flex-col sm:flex-row justify-between items-end border-t border-gray-200 dark:border-gray-800 pt-6 gap-4">
                <div>
                    <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">Target Role</p>
                    <div className="flex items-center gap-2">
                        <span className="material-icons text-gray-400 text-lg">code</span>
                        <p className="font-bold text-lg dark:text-gray-100">Full Stack Developer</p>
                    </div>
                </div>
                <div className="w-full sm:w-64">
                    <div className="flex justify-between text-xs mb-2">
                        <span className="text-gray-500">Live Readiness</span>
                        <span className="text-primary font-bold">71%</span>
                    </div>
                    <div className="h-2.5 w-full bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                        <div className="h-full bg-primary group-data-[is-visible=true]/dashboard:animate-grow-bar rounded-full shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
                    </div>
                </div>
            </div>
        </div>

        {/* Missing Skills & Hiring Accelerator */}
        <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-surface-light/80 dark:bg-card-dark/80 backdrop-blur-md border border-gray-200 dark:border-border-dark rounded-xl p-6 flex flex-col h-full">
                <h4 className="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-5 flex items-center gap-2">
                    <span className="material-icons text-base">warning</span> Top Missing Skills
                </h4>
                <div className="space-y-4 flex-1">
                    {/* Skills List */}
                    {missingSkillsData.map(skill => (
                        <div key={skill.name} className="flex items-center justify-between p-4 rounded-xl bg-white dark:bg-black/40 hover:bg-gray-50 dark:hover:bg-white/5 transition-all group cursor-pointer border border-transparent hover:border-primary/30 shadow-sm transform hover:scale-[1.02]">
                           <div className="flex items-center gap-3">
                               <div className={`p-2 rounded-lg ${skill.colorClass}`}>
                                   <span className="material-icons text-lg">{skill.icon}</span>
                               </div>
                               <span className="font-semibold dark:text-gray-200">{skill.name}</span>
                           </div>
                           <span className="text-xs font-bold bg-primary/10 text-primary py-1.5 px-3 rounded-md group-hover:bg-primary group-hover:text-white transition-colors">{skill.impact}</span>
                       </div>
                    ))}
                </div>
            </div>
            <div className="bg-surface-light/80 dark:bg-card-dark/80 backdrop-blur-md border border-gray-200 dark:border-border-dark rounded-xl p-6 flex flex-col justify-between h-full">
                <div>
                    <h4 className="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                        <span className="material-icons text-base">rocket_launch</span> 30-Day Hiring Accelerator
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-8">Based on your gaps, here is your optimal learning path to reach 70% match.</p>
                    <div className="relative pl-6 border-l-2 border-gray-200 dark:border-gray-700 space-y-8">
                       <div className="relative group">
                            <div className="absolute -left-[31px] top-1 h-4 w-4 rounded-full bg-primary border-4 border-white dark:border-card-dark group-hover:scale-125 transition-transform"></div>
                            <p className="text-xs font-bold text-primary mb-1">WEEK 1</p>
                            <p className="text-base font-bold dark:text-gray-100">Master Server-side Rendering</p>
                        </div>
                        <div className="relative group">
                            <div className="absolute -left-[31px] top-1 h-4 w-4 rounded-full bg-gray-300 dark:bg-gray-600 border-4 border-white dark:border-card-dark group-hover:bg-primary transition-colors"></div>
                            <p className="text-xs font-bold text-gray-500 mb-1">WEEK 2</p>
                            <p className="text-base font-medium text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300 transition-colors">Database Design & ORMs</p>
                        </div>
                    </div>
                </div>
                <button className="mt-8 w-full py-3.5 bg-gray-900 dark:bg-white text-white dark:text-black font-bold rounded-xl text-sm hover:opacity-90 shadow-lg transform hover:-translate-y-0.5 hover:shadow-xl active:scale-95 transition-all flex justify-center items-center gap-2">
                    Start Plan <span className="material-icons text-sm">arrow_forward</span>
                </button>
            </div>
        </div>
    </>
);

const howItWorksData = [
    { icon: 'upload_file', title: 'Upload Syllabus', description: 'Drop your university curriculum PDF. We extract your academic baseline.', colorClass: 'bg-blue-50 dark:bg-blue-900/10 text-blue-600 dark:text-blue-400' },
    { icon: 'work_outline', title: 'Sync Job Interests', description: 'Select your target roles (e.g. "Full Stack dev") to define the goal.', colorClass: 'bg-purple-50 dark:bg-purple-900/10 text-purple-600 dark:text-purple-400' },
    { icon: 'analytics', title: 'Analyze Impact Gap', description: 'Our engine calculates the percentage match and identifies missing skills.', colorClass: 'bg-red-50 dark:bg-red-900/10 text-red-600 dark:text-red-400' },
    { icon: 'rocket_launch', title: 'Execute 30-Day Plan', description: 'Follow the generated roadmap to bridge the gap and get hired.', colorClass: 'bg-emerald-50 dark:bg-emerald-900/10 text-emerald-600 dark:text-emerald-400' },
];

const missingSkillsData = [
    { name: 'Next.js', icon: 'bolt', impact: '+15% Impact', colorClass: 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400' },
    { name: 'PostgreSQL', icon: 'storage', impact: '+8% Impact', colorClass: 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' },
    { name: 'AWS Lambda', icon: 'cloud', impact: '+6% Impact', colorClass: 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400' },
];

export default HowItWorksSection;
