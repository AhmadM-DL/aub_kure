const AboutSection = () => {
    return (
      <section id="about" className="w-full bg-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-black mb-6">About Kure</h2>
          <p className="text-gray-700 text-lg leading-relaxed">
            Kure is a mental health support platform designed to help individuals track and understand their emotional well-being through voice.
            By simply sending WhatsApp voice notes, users can record their thoughts, which are then transcribed, analyzed, and stored using AI.
            Kure detects emotional patterns, tracks mood shifts, and flags signs of suicidal ideation—empowering users and therapists with meaningful insights
            to support ongoing mental health care.
          </p>
        </div>
      </section>
    );
  };
  
  export default AboutSection;
  