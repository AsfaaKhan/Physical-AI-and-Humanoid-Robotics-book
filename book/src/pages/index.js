import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">
          {siteConfig.title}
        </h1>
        <p className="hero__subtitle">
          {siteConfig.tagline}
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Reading 🚀
          </Link>
        </div>
      </div>
    </header>
  );
}

function ModuleCard({ title, description, icon, link }) {
  return (
    <div className={`col col--3 ${styles.moduleCard}`}>
      <div className={styles.cardInner}>
        <div className={styles.cardIcon}>{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
        <Link to={link} className={`button button--primary ${styles.cardButton}`}>
          Explore Module
        </Link>
      </div>
    </div>
  );
}

function ModulesSection() {
  const modules = [
    {
      title: 'Module 1: The Robotic Nervous System (ROS 2)',
      description: 'Learn about Robot Operating System 2, the foundation for robotic applications.',
      icon: '🤖',
      link: '/docs/module-1-ros2/ros2-basics'
    },
    {
      title: 'Module 2: The Digital Twin (Gazebo & Unity)',
      description: 'Explore simulation environments for testing and developing robotic systems.',
      icon: '🎮',
      link: '/docs/module-2-gazebo-unity/gazebo-basics'
    },
    {
      title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      description: 'Discover AI-powered robotics using NVIDIA Isaac platform.',
      icon: '🧠',
      link: '/docs/module-3-isaac/isaac-intro'
    },
    {
      title: 'Module 4: Vision-Language-Action (VLA)',
      description: 'Understand how robots perceive, reason, and act in the physical world.',
      icon: '👁️',
      link: '/docs/module-4-vla/action-generation'
    }
  ];

  return (
    <section className={styles.modulesSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Course Modules</h2>
        <div className="row">
          {modules.map((module, index) => (
            <ModuleCard
              key={index}
              title={module.title}
              description={module.description}
              icon={module.icon}
              link={module.link}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics - Embodied Intelligence and AI in the Physical World">
      <HomepageHeader />
      <main>
        <ModulesSection />
      </main>
    </Layout>
  );
}