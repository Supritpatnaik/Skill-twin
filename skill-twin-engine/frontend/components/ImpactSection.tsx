
import React, { useRef, useEffect, useState } from 'react';
import ScrollAnimatedSection from './ScrollAnimatedSection';

interface AnimatedBarProps {
  width: string;
  className?: string;
}

const AnimatedBar: React.FC<AnimatedBarProps> = ({ width, className }) => {
    const ref = useRef<HTMLDivElement>(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                    observer.unobserve(entry.target);
                }
            },
            { threshold: 0.5 }
        );

        const currentRef = ref.current;
        if (currentRef) {
            observer.observe(currentRef);
        }

        return () => {
            if (currentRef) {
                observer.unobserve(currentRef);
            }
        };
    }, []);

    return (
        <div ref={ref} className="h-4 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div
                className={`h-full bg-gradient-to-r from-primary to-emerald-400 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.4)] transition-all duration-[1.5s] ease-out ${className}`}
                style={{ width: isVisible ? width : '0%' }}
            />
        </div>
    );
};


const skillsData = [
    { name: 'React & Next.js', icon: 'code', iconColor: 'text-blue-500', eligibility: '+45% Eligibility', width: '85%' },
    { name: 'SQL (Advanced Joins)', icon: 'storage', iconColor: 'text-indigo-500', eligibility: '+34% Eligibility', width: '70%' },
    { name: 'Python (Scripting)', icon: 'data_object', iconColor: 'text-yellow-500', eligibility: '+28% Eligibility', width: '55%' },
];

const ImpactSection: React.FC = () => {
    return (
        <>
            <ScrollAnimatedSection className="py-24 bg-surface-light dark:bg-surface-dark">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-2 gap-16 items-center">
                        <div>
                            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-6">Not All Skills Are Equal</h2>
                            <p className="text-lg text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
                                Stop guessing what to learn. Skill-Twin calculates exactly how much each new skill improves your hiring probability based on current demand volume.
                            </p>
                            <ul className="space-y-6">
                                <li className="flex items-start gap-4">
                                    <div className="p-1 bg-primary/10 rounded text-primary"><span className="material-icons text-lg">check</span></div>
                                    <span className="text-gray-700 dark:text-gray-300 font-medium">Real-time data from LinkedIn, Indeed, and Glassdoor.</span>
                                </li>
                                <li className="flex items-start gap-4">
                                    <div className="p-1 bg-primary/10 rounded text-primary"><span className="material-icons text-lg">check</span></div>
                                    <span className="text-gray-700 dark:text-gray-300 font-medium">Weighted scoring based on your specific location.</span>
                                </li>
                                <li className="flex items-start gap-4">
                                    <div className="p-1 bg-primary/10 rounded text-primary"><span className="material-icons text-lg">check</span></div>
                                    <span className="text-gray-700 dark:text-gray-300 font-medium">Personalized for your target role seniority.</span>
                                </li>
                            </ul>
                        </div>
                        <div className="bg-white dark:bg-card-dark p-8 sm:p-10 rounded-3xl shadow-2xl border border-gray-200 dark:border-border-dark hover:border-primary/30 transition-colors">
                            <div className="flex items-center justify-between mb-8">
                                <h3 className="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Impact Simulation: Full Stack Role</h3>
                                <div className="flex gap-2">
                                    <div className="h-3 w-3 rounded-full bg-red-400"></div>
                                    <div className="h-3 w-3 rounded-full bg-yellow-400"></div>
                                    <div className="h-3 w-3 rounded-full bg-green-400"></div>
                                </div>
                            </div>
                            <div className="space-y-8">
                                {skillsData.map((skill, index) => (
                                    <div key={index} className="group">
                                        <div className="flex justify-between mb-3">
                                            <div className="flex items-center gap-2">
                                                <span className={`material-icons ${skill.iconColor}`}>{skill.icon}</span>
                                                <span className="font-bold text-gray-900 dark:text-white">{skill.name}</span>
                                            </div>
                                            <span className="text-primary font-bold bg-primary/5 px-2 py-0.5 rounded text-sm">{skill.eligibility}</span>
                                        </div>
                                        <AnimatedBar width={skill.width} className={index > 0 ? `opacity-${100 - (index * 10)}` : ''}/>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </ScrollAnimatedSection>
            <section className="py-24 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                 <ScrollAnimatedSection>
                    <div className="relative z-10">
                        <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-6 tracking-tight">Ready to close the gap?</h2>
                        <p className="text-xl text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">Stop wasting time learning things that don't matter. Start building the career you want.</p>
                        <button className="bg-primary hover:bg-primary-dark text-white text-lg font-bold py-5 px-12 rounded-xl transition-all shadow-xl shadow-primary/30 hover:shadow-primary/50 hover:shadow-2xl transform hover:-translate-y-1 active:scale-95">
                            Generate My Career Roadmap
                        </button>
                    </div>
                    <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full h-full max-w-2xl bg-gradient-to-t from-primary/10 to-transparent blur-3xl -z-10 pointer-events-none"></div>
                </ScrollAnimatedSection>
            </section>
        </>
    );
};

export default ImpactSection;
