import { useState } from "react";
import { Link, useParams } from "react-router";
import { NotFound } from "../../app/NotFound";
import { useApi } from "../../shared/hooks/useApi";
import styles from "./CertificatePage.module.css";

/** Public verify page. Anyone with the link can check that a certificate is genuine. */
export function CertificatePage() {
  const { code } = useParams();
  const { data: cert, error } = useApi(`/public/certificates/${code}/`);
  if (error?.status === 404) return <NotFound />;
  if (!cert) return <p className="page-loading">Checking the certificate…</p>;

  const revoked = cert.status === "revoked";
  return (
    <div className={`container ${styles.page}`}>
      <p className={revoked ? styles.revoked : styles.verified}>
        {revoked ? `✗ Revoked: ${cert.revoke_reason}` : "✓ Verified certificate"}
      </p>
      {cert.image_url ? (
        <img className={styles.image} src={cert.image_url} alt={`Certificate for ${cert.learner_name}`} />
      ) : (
        <div className={`card ${styles.placeholder}`}>
          <h1>{cert.learner_name}</h1>
          <p>{cert.course_title}</p>
        </div>
      )}
      <dl className={styles.facts}>
        <dt>Learner</dt>
        <dd>{cert.learner_name}</dd>
        <dt>Course</dt>
        <dd>{cert.course_slug ? <Link to={`/${cert.course_slug}`}>{cert.course_title}</Link> : cert.course_title}</dd>
        <dt>Issued</dt>
        <dd>{new Date(cert.issued_at).toLocaleDateString(undefined, { dateStyle: "long" })}</dd>
        <dt>Certificate ID</dt>
        <dd>
          <code>{cert.code}</code>
        </dd>
      </dl>
      {!revoked && <ShareButtons cert={cert} />}
    </div>
  );
}

function ShareButtons({ cert }) {
  const [copied, setCopied] = useState(false);
  const issued = new Date(cert.issued_at);
  const share = encodeURIComponent(cert.share_url);
  const text = encodeURIComponent(`I just completed ${cert.course_title} on ainolez!`);
  const addToProfile = new URLSearchParams({
    startTask: "CERTIFICATION_NAME",
    name: cert.course_title,
    organizationName: "ainolez",
    issueYear: issued.getFullYear(),
    issueMonth: issued.getMonth() + 1,
    certUrl: cert.verify_url,
    certId: cert.code,
  });
  const links = [
    ["Add to LinkedIn profile", `https://www.linkedin.com/profile/add?${addToProfile}`, styles.linkedin],
    ["Post on LinkedIn", `https://www.linkedin.com/sharing/share-offsite/?url=${share}`],
    ["X", `https://twitter.com/intent/tweet?url=${share}&text=${text}`],
    ["Facebook", `https://www.facebook.com/sharer/sharer.php?u=${share}`],
    ["WhatsApp", `https://wa.me/?text=${text}%20${share}`],
    ["Telegram", `https://t.me/share/url?url=${share}&text=${text}`],
  ];

  async function copy() {
    await navigator.clipboard.writeText(cert.verify_url);
    setCopied(true);
  }

  return (
    <section className={styles.share}>
      <h2>Share your achievement</h2>
      <div className={styles.buttons}>
        {links.map(([label, href, className]) => (
          <a key={label} href={href} target="_blank" rel="noreferrer" className={`btn btn-outline ${className ?? ""}`}>
            {label}
          </a>
        ))}
        <button className="btn btn-outline" onClick={copy}>
          {copied ? "Link copied ✓" : "Copy link"}
        </button>
        {cert.pdf_url && (
          <a className="btn btn-primary" href={cert.pdf_url} download>
            Download PDF
          </a>
        )}
      </div>
    </section>
  );
}
