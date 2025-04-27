import Image from "next/image";

const Hero = () => {
  return (
    <section className="w-full bg-white py-15 px-15 sm:px-12 lg:px-20">

      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center">

        {/* Left side - Big Text */}
        <div className="w-full md:w-1/2 px-10 flex justify-center md:justify-start">
          <h1 className="text-4xl md:text-5xl font-bold text-black leading-tight text-center md:text-left">
            Your deserve<br />to be understood and healed.
          </h1>
        </div>

        {/* Right side - Illustration */}
        <div className="w-full md:w-1/2 flex justify-center mt-12 md:mt-0 float-right">
          <div className="relative w-96 h-96">
            <Image
              src="/hero_image.png"
              alt="Hero Image"
              layout="fill"
              objectFit="contain"
              priority
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
