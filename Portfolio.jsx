import React, { useRef } from "react";

const techs = [
  "React",
  "Tailwind CSS",
  "Python",
  "MySQL",
  "FastAPI",
  "Node.js",
];

const projects = [
  {
    title: "Sistema de Gestão Escolar",
    desc: "Plataforma completa para administração de escolas, com módulos de alunos, professores e notas.",
    link: "#",
  },
  {
    title: "Assistente Virtual Zion",
    desc: "Assistente inteligente para automação de tarefas e integração com múltiplos sistemas.",
    link: "#",
  },
  {
    title: "UpSite",
    desc: "Ferramenta para criação rápida de sites modernos e responsivos.",
    link: "#",
  },
];

export default function Portfolio() {
  const sobreRef = useRef(null);
  const projetosRef = useRef(null);
  const contatoRef = useRef(null);

  const scrollTo = (ref) => {
    ref.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="font-sans bg-gray-50 min-h-screen flex flex-col">
      {/* Header */}
      <header className="fixed top-0 left-0 w-full bg-white/80 backdrop-blur z-50 shadow-sm">
        <div className="max-w-5xl mx-auto flex justify-between items-center px-6 py-4">
          <span className="text-2xl font-bold text-gray-800 tracking-tight select-none">Sousa Ezembro</span>
          <nav className="space-x-6">
            <button
              className="text-gray-700 hover:text-blue-600 transition-colors duration-200 font-medium focus:outline-none"
              onClick={() => scrollTo(sobreRef)}
            >
              Sobre
            </button>
            <button
              className="text-gray-700 hover:text-blue-600 transition-colors duration-200 font-medium focus:outline-none"
              onClick={() => scrollTo(projetosRef)}
            >
              Projetos
            </button>
            <button
              className="text-gray-700 hover:text-blue-600 transition-colors duration-200 font-medium focus:outline-none"
              onClick={() => scrollTo(contatoRef)}
            >
              Contato
            </button>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="flex flex-col justify-center items-center text-center min-h-[80vh] pt-32 pb-12 bg-gradient-to-b from-white via-gray-50 to-blue-50">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4 fade-in">Olá, sou Sousa Ezembro</h1>
        <p className="text-lg md:text-xl text-gray-700 mb-8 fade-in delay-100">Desenvolvedor apaixonado por tecnologia e inovação.</p>
        <button
          onClick={() => scrollTo(contatoRef)}
          className="px-8 py-3 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-all duration-200 font-semibold text-lg fade-in delay-200 hover:scale-105 focus:outline-none"
        >
          Fale comigo
        </button>
      </section>

      {/* Sobre */}
      <section ref={sobreRef} className="max-w-3xl mx-auto px-6 py-16" id="sobre">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Sobre</h2>
        <p className="text-gray-700 text-lg mb-6">
          Sou um desenvolvedor apaixonado por tecnologia, com experiência em criação de sistemas web, automações e aplicações modernas. Trabalho com React, Python, MySQL e mais.
        </p>
        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Tecnologias:</h3>
          <ul className="flex flex-wrap gap-3">
            {techs.map((tech) => (
              <li
                key={tech}
                className="bg-blue-100 text-blue-700 px-4 py-1 rounded-full text-sm font-medium shadow-sm hover:bg-blue-200 transition-colors duration-200 fade-in"
              >
                {tech}
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Projetos */}
      <section ref={projetosRef} className="bg-white py-16 px-6" id="projetos">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-800 mb-10">Projetos</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {projects.map((proj, idx) => (
              <div
                key={proj.title}
                className="bg-gray-100 rounded-xl shadow-md p-6 flex flex-col hover:shadow-xl transition-shadow duration-200 fade-in"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <h3 className="text-xl font-semibold text-gray-800 mb-2">{proj.title}</h3>
                <p className="text-gray-600 flex-1 mb-4">{proj.desc}</p>
                <a
                  href={proj.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block mt-auto px-4 py-2 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition-colors duration-200 fade-in hover:scale-105"
                >
                  Ver projeto
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contato */}
      <section ref={contatoRef} className="max-w-2xl mx-auto px-6 py-16" id="contato">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Contato</h2>
        <form
          action="https://formspree.io/f/xgvzkjrw"
          method="POST"
          className="bg-white rounded-xl shadow-md p-8 flex flex-col gap-6 fade-in"
        >
          <div>
            <label htmlFor="nome" className="block text-gray-700 font-medium mb-1">Nome *</label>
            <input
              type="text"
              id="nome"
              name="nome"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none transition-all"
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-gray-700 font-medium mb-1">E-mail *</label>
            <input
              type="email"
              id="email"
              name="email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none transition-all"
            />
          </div>
          <div>
            <label htmlFor="mensagem" className="block text-gray-700 font-medium mb-1">Mensagem *</label>
            <textarea
              id="mensagem"
              name="mensagem"
              required
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none transition-all"
            />
          </div>
          <button
            type="submit"
            className="px-8 py-3 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 transition-all duration-200 fade-in hover:scale-105 focus:outline-none"
          >
            Enviar
          </button>
        </form>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-200 py-6 mt-auto">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between px-6 gap-4">
          <div className="flex gap-6 mb-2 md:mb-0">
            <a
              href="https://github.com/sousaezembro"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-400 transition-colors duration-200 fade-in"
            >
              GitHub
            </a>
            <a
              href="https://linkedin.com/in/sousaezembro"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-400 transition-colors duration-200 fade-in"
            >
              LinkedIn
            </a>
            <a
              href="https://wa.me/258849361638"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-400 transition-colors duration-200 fade-in"
            >
              WhatsApp
            </a>
          </div>
          <span className="text-sm fade-in">&copy; {new Date().getFullYear()} Sousa Ezembro. Todos os direitos reservados.</span>
        </div>
      </footer>

      {/* Fade-in animation styles */}
      <style>{`
        .fade-in {
          opacity: 0;
          transform: translateY(16px);
          animation: fadeInUp 0.7s forwards;
        }
        .fade-in.delay-100 { animation-delay: 0.1s; }
        .fade-in.delay-200 { animation-delay: 0.2s; }
        @keyframes fadeInUp {
          to {
            opacity: 1;
            transform: none;
          }
        }
      `}</style>
    </div>
  );
}
