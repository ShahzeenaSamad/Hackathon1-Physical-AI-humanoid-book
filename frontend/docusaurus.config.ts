import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive interactive textbook for ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://your-vercel-project.vercel.app', // This will be updated after Vercel deployment
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-username', // GitHub org/user name
  projectName: 'physical-ai-textbook', // Repo name

  onBrokenLinks: 'warn', // Allow build with broken links during development

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs', // Serve docs at /docs/ instead of root
          editUrl: undefined, // Disable edit links
        },
        blog: false, // Disable blog feature
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',

    // Chatbot configuration
    chatWidget: {
      backendUrl: 'https://shahzeenasamad-physical-ai-notebook.hf.space', // Hugging Face production backend
      position: 'right',
    },
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/your-username/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1: ROS 2 Fundamentals',
              to: '/docs/module-1-ros2/introduction-physical-ai',
            },
            {
              label: 'Module 2: Gazebo & Unity',
              to: '/docs/module-2-simulation/gazebo-basics',
            },
            {
              label: 'Module 3: NVIDIA Isaac',
              to: '/docs/module-3-isaac/isaac-sim-intro',
            },
            {
              label: 'Module 4: VLA Systems',
              to: '/docs/module-4-vla/vla-overview',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Appendices',
              to: '/docs/appendices/installation-guide',
            },
            {
              label: 'Instructor Guide',
              to: '/docs/appendices/instructor-guide',
            },
          ],
        },
        {
          title: 'Hackathon',
          items: [
            {
              label: 'Panaversity',
              href: 'https://panaversity.com',
            },
            {
              label: 'GitHub Repository',
              href: 'https://github.com/your-username/physical-ai-textbook',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus for Panaversity Hackathon.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
