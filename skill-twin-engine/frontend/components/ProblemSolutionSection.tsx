
import React from 'react';
import ScrollAnimatedSection from './ScrollAnimatedSection';

const problemCards = [
    { icon: 'warning', title: 'Outdated Curriculums', text: 'Most syllabi are updated every 4-5 years. The tech industry reinvents itself every 18 months.', colorClass: 'bg-red-100 dark:bg-red-900/20 text-red-600 dark:text-red-400' },
    { icon: 'visibility_off', title: 'Invisible Skill Gaps', text: "Students don't know what they don't know. Finding out in an interview is too late.", colorClass: 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' },
    { icon: 'gps_fixed', title: 'Generic Advice', text: `"Just learn to code" isn't enough. You need to know which specific framework lands the job.`, colorClass: 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400' },
];

const processSteps = [
    { icon: 'analytics', title: 'Analyze Market', text: 'We scan 50k+ active job listings in your target role.' },
    { icon: 'description', title: 'Extract Skills', text: 'Upload your syllabus. We map your academic learning.' },
    { icon: 'people', title: 'Create Twin', text: 'We build your digital twin and simulate hiring scenarios.' },
    { icon: 'rocket_launch', title: '30-Day Plan', text: 'Get a prioritized roadmap to close the gap fast.' },
];

const ProblemSolutionSection: React.FC = () => {
    return (
        <>
            <section className="py-24 bg-surface-light dark:bg-surface-dark mt-20 relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                    <ScrollAnimatedSection className="text-center max-w-3xl mx-auto mb-16">
                        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">The Syllabus Gap is Real</h2>
                        <p className="text-gray-600 dark:text-gray-400 text-lg">Universities teach theory. Companies hire for application. The mismatch leaves 65% of graduates underemployed.</p>
                    </ScrollAnimatedSection>
                    <div className="grid md:grid-cols-3 gap-8">
                        {problemCards.map((card, index) => (
                            <ScrollAnimatedSection key={index} delay={index * 100} className="bg-white dark:bg-card-dark p-8 rounded-2xl shadow-sm border border-gray-200 dark:border-border-dark hover:border-primary/50 dark:hover:border-primary/50 transition-all transform hover:-translate-y-2 hover:shadow-xl group">
                                <div className={`w-14 h-14 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 group-hover:rotate-3 ${card.colorClass}`}>
                                    <span className="material-icons text-3xl">{card.icon}</span>
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">{card.title}</h3>
                                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{card.text}</p>
                            </ScrollAnimatedSection>
                        ))}
                    </div>
                </div>
            </section>
            <section className="py-24 bg-white dark:bg-background-dark border-t border-gray-200 dark:border-border-dark">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <ScrollAnimatedSection>
                        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-16">From Confusion to Offer Letter</h2>
                    </ScrollAnimatedSection>
                    <ScrollAnimatedSection className="relative">
                        <div className="hidden md:block absolute top-10 left-0 w-full h-0.5 bg-gray-100 dark:bg-gray-800 z-0"></div>
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
                            {processSteps.map((step, index) => (
                                <div key={index} className="text-center group cursor-default">
                                    <div className={`w-20 h-20 mx-auto bg-white dark:bg-card-dark border-4 rounded-full flex items-center justify-center mb-6 transition-all duration-300 z-10 relative group-hover:shadow-[0_0_20px_rgba(16,185,129,0.2)] ${index === 0 ? 'border-primary shadow-[0_0_20px_rgba(16,185,129,0.2)]' : 'border-gray-100 dark:border-gray-800 group-hover:border-primary'}`}>
                                        <span className={`material-icons text-3xl transition-colors ${index === 0 ? 'text-primary' : 'text-gray-400 group-hover:text-primary'}`}>{step.icon}</span>
                                    </div>
                                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{step.title}</h3>
                                    <p className="text-sm text-gray-500 dark:text-gray-400 px-4 leading-relaxed">{step.text}</p>
                                </div>
                            ))}
                        </div>
                    </ScrollAnimatedSection>
                </div>
            </section>
        </>
    );
};

export default ProblemSolutionSection;
