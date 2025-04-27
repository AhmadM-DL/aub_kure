import Header from "./ui/Header";
import Footer from "./ui/Footer";
import Hero from "./ui/Hero";
import Features from "./ui/Features";
import About from "./ui/About";
import Contact from "./ui/Contact";

export default function Home() {
  return (
    <div>
      <Header />
      <Hero />
      <About />
      <Features />
      <Contact />
      <Footer />
    </div>
  );
}
