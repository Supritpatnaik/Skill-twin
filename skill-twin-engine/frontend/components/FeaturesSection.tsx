import React from 'react';
import ScrollAnimatedSection from './ScrollAnimatedSection';

const FeaturesSection: React.FC = () => {
    return (
        <ScrollAnimatedSection className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mt-20">
            <div className="grid md:grid-cols-2 gap-12 items-center">
                <div className="relative group">
                    {/* Glowing background effect */}
                    <div className="absolute -inset-1 bg-gradient-to-r from-primary to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
                    
                    {/* Video Container - Height adjusted to h-full or h-[400px] for better presence */}
                    <div className="relative bg-black rounded-2xl aspect-video flex items-center justify-center border border-gray-100 dark:border-border-dark shadow-xl overflow-hidden">
                        <video
                            autoPlay
                            loop
                            muted
                            playsInline
                            className="w-full h-full object-cover"
                        >
                            <source src="/landing_page.mp4" type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>

                        {/* Glossy overlay to match your UI */}
                        <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-transparent pointer-events-none"></div>
                    </div>
                </div>

                <div className="flex flex-col justify-center">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-300 text-xs font-bold uppercase tracking-wider w-fit mb-4">
                        <span className="material-icons text-sm">auto_graph</span> Hiring Impact
                    </div>
                    <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
                        Turn <span className="text-gray-400 line-through decoration-red-500 decoration-2">Struggling</span> into <span className="text-primary">Strategic</span>.
                    </h2>
                    <p className="text-lg text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
                        Most students learn blindly. Skill-Twin is your unfair advantage. We identify the <span className="font-bold text-gray-900 dark:text-white">exact 3-5 skills</span> standing between you and a top-tier offer letter.
                    </p>
                    
                    {/* Feature list */}
                    <div className="flex flex-col gap-4">
                        <div className="flex items-start gap-4 p-4 rounded-xl bg-surface-light dark:bg-white/5 border border-transparent hover:border-primary/30 transition-all">
                            <div className="bg-primary/10 p-2 rounded-lg text-primary mt-1">
                                <span className="material-icons">psychology</span>
                            </div>
                            <div>
                                <h4 className="font-bold text-gray-900 dark:text-white">Cognitive Mapping</h4>
                                <p className="text-sm text-gray-500 dark:text-gray-400">Your syllabus is parsed and mapped against industry ontologies.</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-4 p-4 rounded-xl bg-surface-light dark:bg-white/5 border border-transparent hover:border-primary/30 transition-all">
                            <div className="bg-primary/10 p-2 rounded-lg text-primary mt-1">
                                <span className="material-icons">engineering</span>
                            </div>
                            <div>
                                <h4 className="font-bold text-gray-900 dark:text-white">Gap Analysis Engine</h4>
                                <p className="text-sm text-gray-500 dark:text-gray-400">We quantify your skill deficit in real-time percentage points.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </ScrollAnimatedSection>
    );
};

export default FeaturesSection;