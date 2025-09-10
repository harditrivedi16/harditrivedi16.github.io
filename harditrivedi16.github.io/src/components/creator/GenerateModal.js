// creater/Generate.js
import React from "react";
import styles from "../../styles/Styles.module.css";

export default function GenerateModal() {
  return (
    <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
      <li className="nav-item">
        <a className="nav-link lead">
          <b>
            <span className={styles.generateWrapper}>
              Generate
              <span className={styles.betaTag}>Beta</span>
            </span>{" "}
            with AI <span className={styles.sparkle}>✨</span>
          </b>
        </a>
      </li>
    </ul>
  );
}

