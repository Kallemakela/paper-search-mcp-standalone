import unittest
import asyncio
from unittest.mock import patch, AsyncMock

from paper_search_mcp import api


class TestDownloadWithFallback(unittest.TestCase):
    def test_repository_fallback_before_scihub(self):
        with patch.object(api.arxiv_searcher, "download_pdf", side_effect=Exception("primary failed")), \
             patch("paper_search_mcp.api._try_repository_fallback", new=AsyncMock(return_value=("/tmp/repo.pdf", ""))), \
             patch("paper_search_mcp.api.SciHubFetcher.download_pdf", side_effect=AssertionError("Sci-Hub should not be called")):
            result = asyncio.run(
                api.download(
                    source="arxiv",
                    paper_id="1234.5678",
                    doi="10.1000/test",
                    title="test",
                    use_scihub=True,
                )
            )
            self.assertEqual(result, "/tmp/repo.pdf")

    def test_unpaywall_fallback_after_repositories(self):
        with patch.object(api.arxiv_searcher, "download_pdf", side_effect=Exception("primary failed")), \
             patch("paper_search_mcp.api._try_repository_fallback", new=AsyncMock(return_value=(None, "repo failed"))), \
             patch.object(api.unpaywall_resolver, "resolve_best_pdf_url", return_value="https://example.org/oa.pdf"), \
             patch("paper_search_mcp.api._download_from_url", new=AsyncMock(return_value="/tmp/unpaywall.pdf")):
            result = asyncio.run(
                api.download(
                    source="arxiv",
                    paper_id="1234.5678",
                    doi="10.1000/test",
                    title="test",
                    use_scihub=True,
                )
            )
            self.assertEqual(result, "/tmp/unpaywall.pdf")

    def test_no_scihub_returns_oa_chain_error(self):
        with patch.object(api.arxiv_searcher, "download_pdf", side_effect=Exception("primary failed")), \
             patch("paper_search_mcp.api._try_repository_fallback", new=AsyncMock(return_value=(None, "repo failed"))), \
             patch.object(api.unpaywall_resolver, "resolve_best_pdf_url", return_value=None):
            result = asyncio.run(
                api.download(
                    source="arxiv",
                    paper_id="1234.5678",
                    doi="10.1000/test",
                    title="test",
                    use_scihub=False,
                )
            )
            self.assertIn("OA fallback chain", result)


if __name__ == "__main__":
    unittest.main()
