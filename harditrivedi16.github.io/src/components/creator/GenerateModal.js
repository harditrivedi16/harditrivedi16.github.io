import React, { useState, useEffect } from "react";
import { Modal, Button, Form, Col } from "react-bootstrap";
import styles from "../../styles/Styles.module.css";
import { LuSparkles } from "react-icons/lu";

export default function GenerateModal() {
    const [showPDFModal, setShowPDFModal] = useState(false);
    const [selectedPDF, setSelectedPDF] = useState(null);
    const [isProcessingAI, setIsProcessingAI] = useState(false); 
      const [pdfUploading, setPdfUploading] = useState(false);

      const handleModalOpen=()=>{
          setShowPDFModal(true); 
      }
    
  return (
    <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
      <li className="nav-item">
        <a className="nav-link lead" onClick={handleModalOpen}>
          <b> 
            <span className={styles.generateWrapper}>
              Generate
              <span className={styles.betaTag}>Beta</span>
            </span>{" "}
            with AI <span> 
              <svg width="20" height="20" viewBox="0 0 24 24">
              <defs>
                <linearGradient id="aiGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#ffffff" />
                  <stop offset="100%" stopColor="#b6ffa2ff" />
                </linearGradient>
              </defs>
              <LuSparkles style={{ fill: "url(#aiGradient)" }} />
            </svg>
            </span>
          </b>
        </a>
      </li>

      <Modal
        show={showPDFModal}
        onHide={() => setShowPDFModal(false)}
        centered
        className={styles.createModal}
      >
        <Modal.Header closeButton>
          <Modal.Title>Upload Your Resume (PDF)</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.File
                label="Choose PDF"
                accept=".pdf"
                onChange={(e) => setSelectedPDF(e.target.files[0])}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowPDFModal(false)}>
            Cancel
          </Button>
          <Button
            variant="primary"
            disabled={!selectedPDF || pdfUploading}
            onClick={async () => {
              setPdfUploading(true);

              // Simulate delay for now
              //await new Promise((res) => setTimeout(res, 2500));

              setPdfUploading(false);
              setShowPDFModal(false);
            }}
          >
            <img
              src="/ai-sparkle-icon.svg" // update if your icon name is different
              alt="AI"
              style={{ width: "1.2rem", marginRight: "0.5rem", marginBottom: "3px" }}
            />
            Generate Portfolio
          </Button>
        </Modal.Footer>
      </Modal>
    </ul>
  );
}

